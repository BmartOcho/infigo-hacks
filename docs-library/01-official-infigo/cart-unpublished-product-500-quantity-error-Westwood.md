# Unpublished product in a customer's cart → cart 500 + "Selected quantity is not available"

**Tags:** cart, basket, shopping-cart, unpublished-product, 500-error, quantity, add-to-cart, impersonation, tier-pricing, westwood, tfresource

## Problem
On tfresource.voomexpress.com, some users got a browser alert plus an inline red banner reading **"Selected quantity is not available. Please select a valid quantity"** (shown twice) when adding *Westwood Pop-Up Tent* (pvId 1046) at qty 1. Other users with identical product settings, the same ConnectID customer code and the same department could add it without trouble.

## Root cause (with evidence)
The failing users had **unpublished products sitting in their shopping carts**. Infigo can't render those lines, so:
- `/cart` returns **HTTP 500** ("We're Sorry, there has been an error!") for any customer holding an unpublished product. Their `/customer/orders` and `/wishlist` pages return 200.
- The add-to-cart step validates against the existing cart, fails, and shows the misleading quantity error.

The product page itself was fine for the failing user (Chelsea List, impersonated). Captured XHRs:
- `GetProductAttributeCombinationDetails` → min 1 / max 1000 / pack 1
- `UpdateQuantityProductPrice` → `isPriceValid: true`, `validationErrors: []`, quote `IsSuccess: true`

So the cause was neither pricing, ConnectID, tier roles nor department. It was data in the user's cart.

## Fix
1. Admin → Customers → (customer) → **Current shopping cart**: delete any unpublished products.
2. Also delete the existing line for the product being added (Chelsea already had a Pop-Up Tent in her cart).
3. Re-add the product. It goes through.

## Sample
Fast triage while impersonating the affected user:
- Open `/cart`. **500 = poisoned cart.** 200 = look elsewhere (tier roles, ConnectID).
- Console one-liner: `fetch('/cart').then(r=>r.status)`

## Caveats
- **Unpublishing a product does not remove it from existing carts.** Every unpublish can poison carts across the storefront. Before unpublishing, check Reports/Customers → shopping carts for that product, or clean carts right after.
- The error text points at quantity/pricing, which is a red herring. Check the cart first whenever an add-to-cart error affects only some users.
- Loading a ConnectID product page creates a new PrintIQ/Infigo quote on each load (82734→82736 during debugging). This is harmless but leaves empty quotes behind.

Related: hack_batch_cart_multiplication.md (other cart-engine behavior)
