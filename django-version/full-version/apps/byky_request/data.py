"""Request Management.

Not an FSD module of its own -- a consolidated approval queue sitting in
front of the individual request workflows the FSD already specifies (FSD
11.1 Wallet Refund Request & Approval Management is the closest existing
precedent for this exact list + approve/reject shape: Claim ID, Customer
Name, Mobile No, amounts, a reason, an approver action panel and a pending/
approved grid). Card Discount Approval is the same pattern applied to a
customer's in-app request for a discount card, tying back into
apps.byky_discount (Card / Card Grade / Card Discount configuration).

No request has ever actually been submitted through the customer mobile app
(FSD Module 9 -- RmsResponsive -- specifies the app but no submissions exist
in any source file), so every list here starts genuinely empty and the
"detail" view is real, working logic with nothing yet to display -- the same
honesty rule as apps.byky_ims.data.unmapped_vehicles() (CLAUDE.md 12).
"""

from apps.byky_discount import data as discount_data

REQUEST_TYPES = ["Card Discount", "Wallet Refund"]
STATUSES = ["Pending", "Approved", "Rejected"]

CARD_TYPES = discount_data.CARD_TYPES


def pending_requests():
    """The consolidated queue across every request type. No source data --
    honest empty list."""
    return []


def card_discount_requests():
    """Card discount requests submitted through the customer app. No source
    data -- honest empty list."""
    return []


def card_discount_request_detail(request_no):
    """A single card discount request's full detail, for the detail view.
    Always None today -- see module docstring."""
    return next((r for r in card_discount_requests() if r["request_no"] == request_no), None)
