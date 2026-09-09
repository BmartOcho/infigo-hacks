#!/usr/bin/env python3
"""
mexgen.py — config-driven MEX generator for Infigo Invent/MegaEdit templates.

A .MEX is a plain ZIP (compression=store) containing PDF assets + template.xml.
The rich model is an embedded JSON at Resources/DataItems/Item[name=InDesignData].
Layout is stored TWICE (XML <Pages> and InDesignData.fields[]) and must stay in
sync — this tool keeps both representations consistent, mints GUIDs/adobeIds,
and repacks a store-zip (built in temp, copied to destination, never overwrites).

Usage:
  py mexgen.py inspect "donor.mex" [--dump DIR]   # inventory report; --dump extracts
                                                  # template.xml + InDesignData.json
  py mexgen.py build config.json                  # generate a new MEX per config

Strategy: clone-donor-node. New variables/fields are deep-copies of a matching
donor prototype with known keys overridden — robust against schema details we
haven't reverse-engineered. Requires the donor to contain at least one TEXT
variable, one TEXT field, and (if IMAGE fields are configured) one IMAGE field.

Stdlib only. Python 3.9+.  (rev 2026-07-01b)
"""

import argparse
import json
import re
import shutil
import sys
import tempfile
import uuid
import zipfile
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path

INDESIGN_ITEM_XPATH = "Resources/DataItems/Item"
TOKEN_RE = re.compile(r"\[#(.+?)#\]")

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def new_guid():
    return str(uuid.uuid4())


def padded_field_id(adobe_id):
    """Donor convention (verified v-01): field id == zero-padded adobeId,
    e.g. adobeId 300 -> '00000000-0000-0000-0000-000000000300'."""
    return "00000000-0000-0000-0000-%012d" % int(adobe_id)


def dynamic_name(name):
    """'Which Example Group?' -> 'Which_Example_Group' (observed convention)."""
    return re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_")


def die(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def warn(msg):
    print("WARN:  " + msg)


def xml_unescape(s):
    return (s.replace("&lt;", "<").replace("&gt;", ">")
             .replace("&quot;", '"').replace("&apos;", "'")
             .replace("&amp;", "&"))  # &amp; last


# ----------------------------------------------------------------------------
# donor loading
# ----------------------------------------------------------------------------

class Donor:
    def __init__(self, mex_path):
        self.path = Path(mex_path)
        if not self.path.exists():
            die("donor not found: %s" % self.path)
        self.zf = zipfile.ZipFile(self.path)
        self.names = self.zf.namelist()
        if "template.xml" not in self.names:
            die("no template.xml in %s" % self.path)
        raw = self.zf.read("template.xml").decode("utf-8-sig")
        self.xml_decl = raw[: raw.index("?>") + 2] if raw.lstrip().startswith("<?xml") else ""
        self.root = ET.fromstring(raw)
        self.idj_item = self._find_indesign_item()
        try:
            self.idj = json.loads(self.idj_item.text or "")
        except (json.JSONDecodeError, TypeError) as e:
            die("cannot parse InDesignData JSON: %s" % e)
        # frozen originals for prototype cloning (before any mutation)
        self.proto = deepcopy(self.idj)

    def _find_indesign_item(self):
        for item in self.root.findall(INDESIGN_ITEM_XPATH):
            if item.get("name") == "InDesignData":
                return item
        die("Resources/DataItems/Item[name=InDesignData] not found")

    # -- structural accessors -------------------------------------------------

    def xml_pages(self):
        pages = self.root.find("Pages")
        if pages is None:
            die("<Pages> not found in template.xml")
        return pages.findall("Page")

    def xml_fields(self):
        """[(page_number_1based, <Field> element, parent <Content>)]"""
        out = []
        for i, page in enumerate(self.xml_pages(), start=1):
            content = page.find("Content")
            if content is None:
                continue
            for f in content.findall("Field"):
                out.append((i, f, content))
        return out

    @staticmethod
    def xml_field_id(field_el):
        el = field_el.find("Information/Id")
        return (el.text or "").strip() if el is not None else ""

    @staticmethod
    def xml_field_name(field_el):
        el = field_el.find("Information/Name")
        return (el.text or "").strip() if el is not None else ""

    def declared_fonts(self):
        return [f.get("name") for f in self.root.findall("Resources/Fonts/Category/Font")
                if f.get("name")]

    def json_fields(self):
        return self.idj.get("fields", [])

    def json_variables(self):
        return self.idj.get("variables", [])

    def form_list(self):
        forms = self.idj.get("forms") or {}
        pages = forms.get("pages") or []
        if not pages:
            return None
        return pages[0].setdefault("form", [])

    # -- prototypes (from frozen original) ------------------------------------

    def proto_variable(self, vtype):
        for v in self.proto.get("variables", []):
            if v.get("type") == vtype:
                return deepcopy(v)
        return None

    def proto_field(self, ftype):
        for f in self.proto.get("fields", []):
            if f.get("type") == ftype:
                return deepcopy(f)
        return None

    def proto_field_by_name(self, name):
        for f in self.proto.get("fields", []):
            if (f.get("field") or {}).get("name") == name:
                return deepcopy(f)
        return None

    def xml_field_by_id(self, fid):
        for _, el, _ in self.xml_fields():
            if self.xml_field_id(el) == fid:
                return el
        return None

    def max_counters(self):
        max_adobe, max_layer = 0, 0
        for f in self.proto.get("fields", []):
            try:
                max_adobe = max(max_adobe, int(f.get("adobeId") or 0))
            except (TypeError, ValueError):
                pass
            try:
                max_layer = max(max_layer, int(f.get("layer") or 0))
            except (TypeError, ValueError):
                pass
        return max_adobe, max_layer


# ----------------------------------------------------------------------------
# inspect
# ----------------------------------------------------------------------------

def cmd_inspect(args):
    d = Donor(args.mex)
    print("== MEX: %s ==" % d.path.name)
    print("\n-- zip entries --")
    for info in d.zf.infolist():
        comp = "STORED" if info.compress_type == zipfile.ZIP_STORED else "DEFLATED"
        print("  %-45s %10d bytes  %s" % (info.filename, info.file_size, comp))

    print("\n-- pages (XML) --")
    for i, p in enumerate(d.xml_pages(), start=1):
        print("  page %d: %s" % (i, dict(p.attrib)))

    print("\n-- declared fonts --")
    for f in d.declared_fonts():
        print("  " + f)
    if not d.declared_fonts():
        print("  (none)")

    print("\n-- variables (JSON) --")
    for v in d.json_variables():
        req = ((v.get("validation") or {}).get("required") or {}).get("enabled")
        print("  %-30s type=%-9s required=%s id=%s" %
              (v.get("name"), v.get("type"), req, v.get("id")))
        for val in v.get("values") or []:
            print("      value: %-20s id=%s" % (val.get("label"), val.get("id")))

    form = d.form_list()
    print("\n-- form order --")
    if form is None:
        print("  (no forms.pages[0].form)")
    else:
        for item in form:
            print("  %-30s type=%s id=%s" % (item.get("label"), item.get("type"), item.get("id")))

    print("\n-- fields (JSON) --")
    xml_ids = {d.xml_field_id(el) for _, el, _ in d.xml_fields()}
    for f in d.json_fields():
        pos = f.get("position") or {}
        name = (f.get("field") or {}).get("name")
        fv = f.get("fieldValue")
        in_xml = "yes" if f.get("id") in xml_ids else "NO-XML-MATCH"
        print("  %-28s type=%-6s page=%s pos=(%.1f,%.1f %sx%s) adobeId=%s layer=%s xml=%s" %
              (name, f.get("type"), f.get("page"),
               pos.get("x", -1), pos.get("y", -1), pos.get("width"), pos.get("height"),
               f.get("adobeId"), f.get("layer"), in_xml))
        if fv:
            print("      fieldValue: %r" % fv)

    print("\n-- logicRules (JSON) --")
    rules = d.idj.get("logicRules") or []
    print("  %d rule(s)" % len(rules))
    for r in rules:
        print("  " + (r.get("name") or "(unnamed)"))

    if args.dump:
        out = Path(args.dump)
        out.mkdir(parents=True, exist_ok=True)
        (out / "template.xml").write_bytes(d.zf.read("template.xml"))
        (out / "InDesignData.json").write_text(
            json.dumps(d.idj, indent=2), encoding="utf-8")
        print("\nDumped template.xml + InDesignData.json -> %s" % out)


# ----------------------------------------------------------------------------
# build
# ----------------------------------------------------------------------------

def load_config(cfg_path):
    p = Path(cfg_path)
    if not p.exists():
        die("config not found: %s" % p)
    cfg = json.loads(p.read_text(encoding="utf-8-sig"))
    cfg["_dir"] = p.parent
    for key in ("donor", "output"):
        if not cfg.get(key):
            die("config missing '%s'" % key)
    for f in cfg.get("fields", []):
        for v in (f.get("cloneFrom"), f.get("asset")):
            if isinstance(v, str) and "TODO" in v.upper():
                die("field '%s' still has a TODO placeholder — run inspect first "
                    "and fill in real donor names" % f.get("name"))
    return cfg


class Builder:
    def __init__(self, cfg):
        self.cfg = cfg
        self.donor = Donor(cfg["_dir"] / cfg["donor"])
        self.idj = self.donor.idj          # mutated in place
        self.root = self.donor.root        # mutated in place
        self.adobe_ctr, self.layer_ctr = self.donor.max_counters()
        self.stack_counters = {}
        self.var_by_name = {}              # display name -> variable dict
        self.new_fields = []               # (json_field, xml_element) for validation
        self.errors = []

    # -- counters --------------------------------------------------------

    def next_adobe(self):
        self.adobe_ctr += 1
        return self.adobe_ctr

    def next_layer(self):
        self.layer_ctr += 1
        return self.layer_ctr

    # -- strip (replace mode) ---------------------------------------------

    def strip(self):
        keep = set(self.cfg.get("keepFields") or [])
        kept_ids = set()
        new_json_fields = []
        for f in self.donor.json_fields():
            name = (f.get("field") or {}).get("name")
            if name in keep:
                new_json_fields.append(f)
                kept_ids.add(f.get("id"))
        self.idj["fields"] = new_json_fields

        for _, el, content in self.donor.xml_fields():
            if Donor.xml_field_id(el) not in kept_ids:
                content.remove(el)

        self.idj["variables"] = []
        self.idj["logicRules"] = []
        form = self.donor.form_list()
        if form is not None:
            del form[:]

        missing = keep - {(f.get("field") or {}).get("name") for f in new_json_fields}
        if missing:
            self.errors.append("keepFields not found in donor: %s" % sorted(missing))

    # -- variables ---------------------------------------------------------

    def add_variables(self):
        for vcfg in self.cfg.get("variables", []):
            vtype = (vcfg.get("type") or "TEXT").upper()
            proto = self.donor.proto_variable(vtype)
            if proto is None:
                self.errors.append("no donor prototype for variable type %s "
                                   "(needed by '%s')" % (vtype, vcfg.get("name")))
                continue
            v = proto
            v["id"] = new_guid()
            v["name"] = vcfg["name"]
            v["dynamicName"] = dynamic_name(vcfg["name"])
            validation = v.setdefault("validation", {})
            validation["required"] = {
                "enabled": bool(vcfg.get("required", False)),
                "message": vcfg.get("message", "Required"),
            }
            # prefill is handled product-level by the Prepopulate Data Script,
            # not per-variable — force no variable-level prepopulation.
            if "prepopulation" in v and isinstance(v["prepopulation"], dict):
                v["prepopulation"]["mode"] = "Nothing"
            if vtype == "DROPDOWN":
                vals = vcfg.get("values") or []
                if not vals:
                    self.errors.append("dropdown '%s' has no values" % vcfg["name"])
                v["values"] = [{"id": new_guid(), "label": x, "value": x} for x in vals]
                v["defaultValue"] = int(vcfg.get("defaultIndex", 0))
            else:
                v["defaultValue"] = vcfg.get("default", "")
                v.pop("values", None)
            self.idj["variables"].append(v)
            self.var_by_name[v["name"]] = v

    def add_form(self):
        form = self.donor.form_list()
        if form is None:
            self.errors.append("donor has no forms.pages[0].form to populate")
            return
        for label in self.cfg.get("form", []):
            v = self.var_by_name.get(label)
            if v is None:
                self.errors.append("form entry '%s' is not a configured variable" % label)
                continue
            form.append({"id": v["id"], "type": "ITEM", "label": v["name"]})

    # -- geometry ----------------------------------------------------------

    def resolve_position(self, fcfg):
        """Returns dict with x,y,width,height,angle or None (= keep clone's)."""
        if fcfg.get("position"):
            p = dict(fcfg["position"])
            p.setdefault("angle", 0)
            return p
        if fcfg.get("positionFrom"):
            src = self.donor.proto_field_by_name(fcfg["positionFrom"])
            if src is None:
                self.errors.append("positionFrom '%s' not found in donor (field '%s')"
                                   % (fcfg["positionFrom"], fcfg.get("name")))
                return None
            return dict(src.get("position") or {})
        if fcfg.get("stack"):
            stacks = self.cfg.get("stacks") or {}
            s = stacks.get(fcfg["stack"])
            if s is None:
                self.errors.append("unknown stack '%s' (field '%s')"
                                   % (fcfg["stack"], fcfg.get("name")))
                return None
            idx = self.stack_counters.get(fcfg["stack"], 0)
            self.stack_counters[fcfg["stack"]] = idx + 1
            return {
                "x": s["x"],
                "y": s["yStart"] + idx * s["lineHeight"],
                "width": s["width"],
                "height": s["height"],
                "angle": 0,
            }
        return None  # image clones fall back to prototype position

    def apply_xml_position(self, field_el, pos, field_name=""):
        if pos is None:
            return
        pel = field_el.find("Position")
        if pel is None:
            self.errors.append("cloned XML field has no <Position> ('%s')" % field_name)
            return
        keymap = {k.lower(): k for k in pel.attrib}
        matched = 0
        for want, val in (("x", pos.get("x")), ("y", pos.get("y")),
                          ("width", pos.get("width")), ("height", pos.get("height")),
                          ("angle", pos.get("angle", 0))):
            if val is None:
                continue
            actual = keymap.get(want)
            if actual is not None:
                pel.set(actual, str(val))
                matched += 1
        if matched < 2:  # x and y at minimum should have matched
            self.errors.append("XML <Position> attrs %s did not match expected x/y/width/"
                               "height on field '%s' — donor uses a different naming; "
                               "report the attr names from inspect" %
                               (sorted(pel.attrib), field_name))

    # -- fields ------------------------------------------------------------

    def xml_content_for_page(self, page_num):
        pages = self.donor.xml_pages()
        if not (1 <= page_num <= len(pages)):
            self.errors.append("page %s out of range (donor has %d pages)"
                               % (page_num, len(pages)))
            return None
        content = pages[page_num - 1].find("Content")
        if content is None:
            content = ET.SubElement(pages[page_num - 1], "Content")
        return content

    def _set_xml_information(self, el, guid, name):
        info = el.find("Information")
        if info is None:
            self.errors.append("cloned XML field has no <Information> (field '%s')" % name)
            return
        for tag, val in (("Id", guid), ("Name", name)):
            child = info.find(tag)
            if child is not None:
                child.text = val
        # CustomData is a JSON text blob: {"originalFieldId": "<id>"} (verified v-01)
        cd = info.find("CustomData")
        if cd is not None:
            try:
                data = json.loads(cd.text or "{}")
            except json.JSONDecodeError:
                data = {}
            data["originalFieldId"] = guid
            cd.text = json.dumps(data, indent=4)

    def add_text_field(self, fcfg):
        # protoFrom: clone a specific donor field by name (inherits its full look);
        # otherwise clone the first TEXT field found.
        proto_name = fcfg.get("protoFrom")
        proto_j = (self.donor.proto_field_by_name(proto_name) if proto_name
                   else self.donor.proto_field("TEXT"))
        if proto_j is None:
            self.errors.append("donor TEXT prototype not found (protoFrom=%s, field '%s')"
                               % (proto_name, fcfg.get("name")))
            return
        # replace mode strips the proto's live XML twin — use the pre-strip cache
        proto_x = self._prestrip_xml_proto_by_id(proto_j.get("id")) or \
            self._prestrip_xml_proto("text")
        if proto_x is None:
            self.errors.append("no donor XML <Field type='text'> available to clone")
            return

        page = int(fcfg.get("page", 1))       # config: 1-based, human-friendly
        pos = self.resolve_position(fcfg)
        if pos is None:
            self.errors.append("text field '%s' needs 'position', 'positionFrom', or "
                               "'stack'" % fcfg.get("name"))
            return
        value = fcfg.get("value", "")
        adobe = self.next_adobe()
        guid = padded_field_id(adobe)         # donor convention: id == padded adobeId

        # ---- JSON twin
        j = proto_j
        j["id"] = guid
        j["adobeId"] = adobe
        j["layer"] = self.next_layer()
        j["page"] = page - 1                  # JSON page is 0-based (verified v-01)
        if pos:
            j["position"] = pos
        j["fieldValue"] = value
        fld = j.setdefault("field", {})
        fld["name"] = fcfg["name"]
        fld["visible"] = bool(fcfg.get("visible", True))
        fontcfg = fcfg.get("font") or {}
        size = fontcfg.get("size")
        # JSON text.format.fontSize stays as the clone's (donor keeps INHERIT there
        # even when XML <FontSize> carries the real value — XML is authoritative).
        self.idj["fields"].append(j)

        # ---- XML twin
        x = deepcopy(proto_x)
        self.apply_xml_position(x, pos, fcfg["name"])
        text_el = x.find("Data/Text")
        if text_el is not None:
            text_el.text = value
        else:
            self.errors.append("cloned XML text field lacks Data/Text ('%s')" % fcfg["name"])
        font_name = fontcfg.get("name")
        if font_name == "AUTO":
            fonts = self.donor.declared_fonts()
            font_name = fonts[0] if fonts else None
        if font_name and font_name != "INHERIT":
            fel = x.find("Data/Format/Font")
            if fel is not None:
                fel.set("name", font_name)
        if size is not None and size != "INHERIT":
            sel = x.find("Data/Format/FontSize")
            if sel is not None:
                sel.text = str(size)
        for tag, key in (("HorizontalAlignment", "hAlign"), ("VerticalAlignment", "vAlign"),
                         ("TextColor", "colorCMYK")):
            if fontcfg.get(key) is not None:
                el = x.find("Data/Format/" + tag)
                if el is not None:
                    el.text = str(fontcfg[key])
        # raw escape hatch: {"xmlFormat": {"Leading": "12", ...}}
        for tag, val in (fcfg.get("xmlFormat") or {}).items():
            el = x.find("Data/Format/" + tag)
            if el is not None:
                el.text = str(val)
        self._set_xml_information(x, guid, fcfg["name"])
        content = self.xml_content_for_page(page)
        if content is not None:
            content.append(x)
        self.new_fields.append((j, x))

    def find_clipart_item(self, asset_basename):
        """Locate a clipart resource item by file basename in JSON resources.Clipart.
        Returns (setId, itemId) or None."""
        for rset in (self.donor.proto.get("resources") or {}).get("Clipart") or []:
            for item in rset.get("items") or []:
                if ((item.get("file") or {}).get("name")) == asset_basename:
                    return rset.get("id"), item.get("id")
        return None

    def add_image_field(self, fcfg):
        src_name = fcfg.get("cloneFrom")
        proto_j = (self.donor.proto_field_by_name(src_name) if src_name
                   else self.donor.proto_field("IMAGE"))
        if proto_j is None:
            self.errors.append("no donor IMAGE field to clone (field '%s', cloneFrom=%s)"
                               % (fcfg.get("name"), src_name))
            return
        proto_x = self._prestrip_xml_proto_by_id(proto_j.get("id"))
        if proto_x is None:
            proto_x = self._prestrip_xml_proto("image")
        if proto_x is None:
            self.errors.append("no donor XML twin for image field '%s'" % src_name)
            return

        pos = self.resolve_position(fcfg)     # None -> keep prototype geometry
        adobe = self.next_adobe()
        guid = padded_field_id(adobe)
        # config page 1-based; default = prototype's (already 0-based JSON)
        if fcfg.get("page") is not None:
            jpage = int(fcfg["page"]) - 1
        else:
            jpage = int(proto_j.get("page", 0))

        j = proto_j
        j["id"] = guid
        j["adobeId"] = adobe
        j["layer"] = self.next_layer()
        j["page"] = jpage
        if pos:
            j["position"] = pos
        j.setdefault("field", {})["name"] = fcfg["name"]

        # Pin an asset via clipart resource reference. EXPERIMENTAL: shape inferred
        # from v-01's SetImage action value {value:<itemId>, resourceSet:<setId>,
        # option:"RESOURCE"} — prefer the assetContentSwap background mechanism
        # (fully verified) when the art fills the page.
        new_asset = fcfg.get("asset")
        if new_asset:
            hit = self.find_clipart_item(Path(new_asset).name)
            if hit is None:
                self.errors.append("image field '%s': asset '%s' not found in donor "
                                   "resources.Clipart" % (fcfg.get("name"), new_asset))
            else:
                set_id, item_id = hit
                img = j.setdefault("image", {})
                img["imageValue"] = {"type": "RESOURCE",
                                     "value": {"resourceSet": set_id, "value": item_id}}
                warn("image field '%s': RESOURCE imageValue shape is inferred, not "
                     "verified — import-test before trusting" % fcfg.get("name"))
        self.idj["fields"].append(j)

        x = deepcopy(proto_x)
        self.apply_xml_position(x, pos, fcfg["name"])
        self._set_xml_information(x, guid, fcfg["name"])
        content = self.xml_content_for_page(jpage + 1)
        if content is not None:
            content.append(x)
        self.new_fields.append((j, x))

    # pre-strip XML prototype cache -----------------------------------------

    def cache_xml_protos(self):
        """Call BEFORE strip(): keep deep copies of one XML field per type attr
        and every field element by id, so clones survive replace-mode removal."""
        self._xml_by_type = {}
        self._xml_by_id = {}
        for _, el, _ in self.donor.xml_fields():
            t = (el.get("type") or "").lower()
            if t and t not in self._xml_by_type:
                self._xml_by_type[t] = deepcopy(el)
            fid = Donor.xml_field_id(el)
            if fid:
                self._xml_by_id[fid] = deepcopy(el)

    def _prestrip_xml_proto(self, type_attr):
        return deepcopy(self._xml_by_type.get(type_attr))

    def _prestrip_xml_proto_by_id(self, fid):
        el = self._xml_by_id.get(fid)
        return deepcopy(el) if el is not None else None

    # -- edit-mode ops (donor kept intact, surgical changes) -----------------

    @staticmethod
    def _form_leaf_vid(item):
        return item.get("variableID") or item.get("id")

    def _form_prune(self, removed_ids):
        def prune(items):
            out = []
            for it in items:
                if it.get("type") == "GROUP":
                    it["items"] = prune(it.get("items") or [])
                    out.append(it)
                elif self._form_leaf_vid(it) not in removed_ids:
                    out.append(it)
            return out
        form = self.donor.form_list()
        if form is not None:
            form[:] = prune(form)

    def op_remove_variables(self):
        names = set(self.cfg.get("removeVariables") or [])
        if not names:
            return
        have = {v["name"] for v in self.idj.get("variables", [])}
        missing = names - have
        if missing:
            self.errors.append("removeVariables not in donor: %s" % sorted(missing))
        removed_ids = {v["id"] for v in self.idj["variables"] if v["name"] in names}
        self.idj["variables"] = [v for v in self.idj["variables"]
                                 if v["name"] not in names]
        self._form_prune(removed_ids)

    def op_form_add(self):
        """formAdd: [{"name": "<variable display name>", "after": "<existing item
        name/label>"}] — inserts an ITEM next to a sibling, mirroring its key shape."""
        for spec in self.cfg.get("formAdd") or []:
            v = self.var_by_name.get(spec["name"]) or next(
                (x for x in self.idj.get("variables", [])
                 if x["name"] == spec["name"]), None)
            if v is None:
                self.errors.append("formAdd '%s' is not a variable" % spec.get("name"))
                continue

            def insert(items):
                for i, it in enumerate(items):
                    label = it.get("label") or it.get("name")
                    if it.get("type") == "ITEM" and label == spec.get("after"):
                        new = {"id": v["id"], "type": "ITEM"}
                        if "variableID" in it:
                            new.update({"variableID": v["id"], "name": v["name"],
                                        "batchSource": False})
                        if "label" in it:
                            new["label"] = v["name"]
                        items.insert(i + 1, new)
                        return True
                    if it.get("type") == "GROUP" and insert(it.get("items") or []):
                        return True
                return False

            form = self.donor.form_list()
            if form is None or not insert(form):
                self.errors.append("formAdd: anchor '%s' not found for '%s'"
                                   % (spec.get("after"), spec.get("name")))

    def op_edit_fields(self):
        """editFields: [{"adobeId": 343, "value": "<new fieldValue>"}] — rewrites a
        donor field's content in BOTH representations, everything else untouched."""
        for spec in self.cfg.get("editFields") or []:
            target = next((f for f in self.idj.get("fields", [])
                           if f.get("adobeId") == spec.get("adobeId")), None)
            if target is None:
                self.errors.append("editFields: adobeId %s not found" % spec.get("adobeId"))
                continue
            target["fieldValue"] = spec["value"]
            xel = self.donor.xml_field_by_id(target.get("id"))
            tel = xel.find("Data/Text") if xel is not None else None
            if tel is None:
                self.errors.append("editFields: no XML Data/Text for adobeId %s"
                                   % spec.get("adobeId"))
                continue
            tel.text = spec["value"]
            self.new_fields.append((target, xel))  # reuse text-parity validation

    def op_clipart_rename(self):
        """clipartRename: {"OldName": "NewName"} — renames an XML clipart resource
        and every ClipartImage reference; BinaryReference repointed to
        ./cliparts/<NewName>.pdf. Pair with assetsRemove (old pdf) + assetsAdd
        (new pdf named <NewName>.pdf). Run BEFORE asset pruning."""
        renames = self.cfg.get("clipartRename") or {}
        for old, new in renames.items():
            hits = 0
            grp = self.root.find("Resources/Cliparts")
            for cat in (grp.findall("Category") if grp is not None else []):
                for c in cat.findall("Clipart"):
                    if c.get("name") == old:
                        c.set("name", new)
                        br = c.find("BinaryReference")
                        if br is not None:
                            br.text = "./cliparts/%s.pdf" % new
                        hits += 1
            for ci in self.root.iter("ClipartImage"):
                if ci.get("name") == old:
                    ci.set("name", new)
                    hits += 1
            if hits == 0:
                self.errors.append("clipartRename: '%s' not found in XML" % old)

    # -- logic (deliberately unsupported for now) ---------------------------

    def check_logic(self):
        if self.cfg.get("logic"):
            self.errors.append("config has logic rules — logicRule generation is not "
                               "implemented yet (this build needs none; ask Claude to "
                               "extend mexgen when a rule-based product comes up)")

    # -- assets --------------------------------------------------------------

    def asset_plan(self):
        remove = set(self.cfg.get("assetsRemove") or [])
        keep = [n for n in self.donor.names if n not in remove and n != "template.xml"]
        gone = remove - set(self.donor.names)
        if gone:
            warn("assetsRemove entries not in donor (ignored): %s" % sorted(gone))
        adds = []
        for a in self.cfg.get("assetsAdd") or []:
            src = self.cfg["_dir"] / a
            if not src.exists():
                self.errors.append("assetsAdd file missing: %s" % src)
            else:
                adds.append(src)
        # assetContentSwap: {"target/entry.pdf": "source/entry.pdf"} — target keeps
        # its zip name but is written with the source entry's BYTES. Verified-safe
        # way to repoint a background at different artwork without touching schema.
        swap = dict(self.cfg.get("assetContentSwap") or {})
        for tgt, src in swap.items():
            if tgt not in self.donor.names:
                self.errors.append("assetContentSwap target '%s' not in donor" % tgt)
            if src not in self.donor.names:
                self.errors.append("assetContentSwap source '%s' not in donor" % src)
            if tgt in remove:
                self.errors.append("assetContentSwap target '%s' is also in "
                                   "assetsRemove" % tgt)
        if remove:
            self.prune_resources(remove)
        return keep, adds, swap

    def prune_resources(self, removed_entries):
        """Remove XML + JSON resource declarations that point at removed zip entries
        (dangling BinaryReferences could fail import)."""
        basenames = {Path(r).name for r in removed_entries}
        # JSON resources.Clipart items
        for rset in (self.idj.get("resources") or {}).get("Clipart") or []:
            items = rset.get("items") or []
            rset["items"] = [it for it in items
                             if (it.get("file") or {}).get("name") not in basenames]
        # XML Cliparts / Backgrounds with matching BinaryReference
        for group, tag in (("Resources/Cliparts", "Clipart"),
                           ("Resources/Backgrounds", "Background")):
            grp = self.root.find(group)
            if grp is None:
                continue
            for cat in grp.findall("Category"):
                for el in cat.findall(tag):
                    ref = (el.findtext("BinaryReference") or "").strip()
                    if ref and Path(ref).name in basenames:
                        cat.remove(el)

    # -- validation ------------------------------------------------------------

    def validate(self, final_names):
        errs = list(self.errors)
        var_names = {v["name"] for v in self.idj.get("variables", [])}
        var_ids = {v["id"] for v in self.idj.get("variables", [])}

        for f in self.idj.get("fields", []):
            fv = f.get("fieldValue") or ""
            for tok in TOKEN_RE.findall(fv):
                if tok not in var_names:
                    errs.append("token [#%s#] in field '%s' has no matching variable"
                                % (tok, (f.get("field") or {}).get("name")))

        def check_form(items):
            for item in items:
                if item.get("type") == "GROUP":
                    check_form(item.get("items") or [])
                elif self._form_leaf_vid(item) not in var_ids:
                    errs.append("form item '%s' id does not match any variable"
                                % (item.get("label") or item.get("name")))
        check_form(self.donor.form_list() or [])

        # XML/JSON parity by id
        json_ids = {f.get("id") for f in self.idj.get("fields", [])}
        xml_ids = {Donor.xml_field_id(el) for _, el, _ in self.donor.xml_fields()}
        for missing in sorted(json_ids - xml_ids):
            errs.append("field id %s present in JSON but not XML" % missing)
        for missing in sorted(xml_ids - json_ids):
            errs.append("field id %s present in XML but not JSON" % missing)

        # token text parity for the fields we added
        for j, x in self.new_fields:
            tel = x.find("Data/Text")
            if tel is not None and (tel.text or "") != (j.get("fieldValue") or ""):
                errs.append("XML/JSON text mismatch on field '%s'"
                            % (j.get("field") or {}).get("name"))

        # configured assets must exist in final zip
        for fcfg in self.cfg.get("fields", []):
            a = fcfg.get("asset")
            if a and a not in final_names:
                errs.append("field '%s' references asset '%s' not present in output zip"
                            % (fcfg.get("name"), a))

        all_names = [v["name"] for v in self.idj.get("variables", [])]
        dupes = sorted({n for n in all_names if all_names.count(n) > 1})
        if dupes:
            errs.append("duplicate variable names: %s" % dupes)
        return errs

    # -- serialize + pack -------------------------------------------------------

    def serialize_xml(self):
        # re-embed InDesignData JSON
        self.donor.idj_item.text = json.dumps(self.idj)
        body = ET.tostring(self.root, encoding="unicode")

        # restore CDATA on rich-text bodies (ET escaped them)
        def cdata(m):
            return m.group(1) + "<![CDATA[" + xml_unescape(m.group(2)) + "]]>" + m.group(3)

        body = re.sub(r'(<Text[^>]*isRichText="true"[^>]*>)(.*?)(</Text>)',
                      cdata, body, flags=re.S)
        # restore CDATA on the InDesignData item
        body = re.sub(r'(<Item[^>]*name="InDesignData"[^>]*>)(.*?)(</Item>)',
                      cdata, body, flags=re.S)
        decl = self.donor.xml_decl or '<?xml version="1.0" encoding="utf-8"?>'
        return decl + "\n" + body

    def pack(self, xml_text, keep_names, add_paths, swap=None):
        swap = swap or {}
        out_rel = self.cfg["output"]
        dest = self.cfg["_dir"] / out_rel
        if dest.exists():
            die("output already exists (fresh filenames only): %s" % dest)
        tmpdir = Path(tempfile.mkdtemp(prefix="mexgen_"))
        tmp_zip = tmpdir / dest.name
        try:
            with zipfile.ZipFile(tmp_zip, "w", compression=zipfile.ZIP_STORED) as z:
                z.writestr("template.xml", xml_text.encode("utf-8"))
                for name in keep_names:
                    if name.endswith("/"):
                        continue
                    source_entry = swap.get(name, name)
                    z.writestr(name, self.donor.zf.read(source_entry))
                for src in add_paths:
                    arc = ("cliparts/" + src.name) if src.suffix.lower() == ".pdf" and \
                        not any(src.name == Path(k).name for k in keep_names) else src.name
                    z.write(src, arc)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(tmp_zip, dest)  # build in tmp, copy to folder (never zip in place)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
        return dest


def cmd_build(args):
    cfg = load_config(args.config)
    b = Builder(cfg)

    b.cache_xml_protos()
    mode = (cfg.get("mode") or "replace").lower()
    if mode == "replace":
        b.strip()
    elif mode not in ("add", "edit"):
        die("mode must be 'replace', 'add', or 'edit'")

    if mode == "edit":
        # surgical: donor kept intact, then rename/remove/add/edit
        b.op_clipart_rename()      # before asset pruning (repoints BinaryReference)
        b.op_remove_variables()
        b.add_variables()          # cfg 'variables' = variables to ADD in edit mode
        b.op_form_add()
        b.op_edit_fields()
    else:
        b.add_variables()
        b.add_form()
    for fcfg in cfg.get("fields", []):
        ftype = (fcfg.get("type") or "TEXT").upper()
        if ftype == "TEXT":
            b.add_text_field(fcfg)
        elif ftype == "IMAGE":
            b.add_image_field(fcfg)
        else:
            b.errors.append("unsupported field type %s ('%s')" % (ftype, fcfg.get("name")))
    b.check_logic()

    keep_names, add_paths, swap = b.asset_plan()
    final_names = set(keep_names) | {("cliparts/" + p.name) for p in add_paths} | \
        {p.name for p in add_paths} | {"template.xml"}

    errs = b.validate(final_names)
    if errs:
        print("VALIDATION FAILED — no file written:")
        for e in errs:
            print("  - " + e)
        sys.exit(2)

    xml_text = b.serialize_xml()
    dest = b.pack(xml_text, keep_names, add_paths, swap)
    print("OK: wrote %s" % dest)
    print("    variables=%d  form items=%d  fields=%d (json)  assets kept=%d added=%d"
          % (len(b.idj.get("variables", [])), len(b.donor.form_list() or []),
             len(b.idj.get("fields", [])), len(keep_names), len(add_paths)))
    print("    Import into MegaEdit to finish validation (import errors are invisible "
          "until tested).")


# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Config-driven MEX generator")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_i = sub.add_parser("inspect", help="inventory a donor MEX")
    p_i.add_argument("mex")
    p_i.add_argument("--dump", help="directory to extract template.xml + InDesignData.json")
    p_i.set_defaults(func=cmd_inspect)
    p_b = sub.add_parser("build", help="build a MEX from a config JSON")
    p_b.add_argument("config")
    p_b.set_defaults(func=cmd_build)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
