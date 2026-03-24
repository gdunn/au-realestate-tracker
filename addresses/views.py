from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Address
from .utils import update_property_info


# simple list view for addresses; sorting is controlled via the ``sort``
# query parameter, which currently supports ``date`` (default) and ``suburb``.
#
# - ``date`` sorts by the time the record was entered (newest first).
# - ``suburb`` sorts alphabetically by suburb.
#
# This view also handles POST submissions from the front end:
#   * a form that creates a new address
#
# Deletions are submitted to ``address_delete`` (below), which requires a POST
# to avoid accidental GET deletions.
@login_required
def address_list(request):
    if request.method == "POST":
        # creation form submitted
        address_input = request.POST.get("address_input", "").strip()
        if address_input:
            # Parse the input: support "street, suburb state", "street, suburb state", etc.
            street = ""
            suburb = ""
            state = ""

            if "," in address_input:
                parts = address_input.split(",", 1)
                street = parts[0].strip()
                remainder = parts[1].strip() if len(parts) > 1 else ""
            elif "\t" in address_input:
                parts = address_input.split("\t", 1)
                street = parts[0].strip()
                remainder = parts[1].strip() if len(parts) > 1 else ""
            else:
                # Fallback: assume "street suburb state" format
                parts = address_input.rsplit(" ", 2)
                if len(parts) >= 2:
                    street = parts[0].strip()
                    suburb = parts[1].strip()
                    if len(parts) >= 3:
                        state = parts[2].strip()
                else:
                    street = address_input
                    suburb = ""
                    state = ""

            # If we have a remainder, try to split it into suburb and state
            if "remainder" in locals() and remainder:
                remainder_parts = remainder.rsplit(" ", 1)
                if len(remainder_parts) >= 2:
                    potential_state = remainder_parts[1].strip()
                    # Check if the last part looks like a state abbreviation
                    australian_states = [
                        "NSW",
                        "VIC",
                        "QLD",
                        "WA",
                        "SA",
                        "TAS",
                        "ACT",
                        "NT",
                    ]
                    if potential_state.upper() in australian_states:
                        suburb = remainder_parts[0].strip()
                        state = potential_state.upper()
                    else:
                        # Not a state, treat whole remainder as suburb
                        suburb = remainder
                else:
                    suburb = remainder

            if street:
                Address.objects.create(
                    street_address=street, suburb=suburb, state=state
                )
        # redirect to avoid duplicate POST on refresh
        return redirect(reverse("address_list"))

    sort = request.GET.get("sort")
    if sort == "suburb":
        addresses = Address.objects.order_by("suburb")
    else:
        # default to date; show newest first
        addresses = Address.objects.order_by("-created_at")

    # include the current default state for the form
    from .models import AddressConfig

    default_state = AddressConfig.get_default_state()

    return render(
        request,
        "addresses/address_list.html",
        {"addresses": addresses, "default_state": default_state},
    )


@login_required
def address_delete(request, pk):
    # simply remove the object and redirect back
    if request.method == "POST":
        addr = get_object_or_404(Address, pk=pk)
        addr.delete()
    return redirect(reverse("address_list"))


@login_required
def scrape_property(request, pk):
    """AJAX endpoint to scrape property information for an address."""
    if request.method == "POST":
        address = get_object_or_404(Address, pk=pk)
        try:
            results = update_property_info(address)
            return JsonResponse(
                {
                    "success": True,
                    "message": f"Scraped property info from {len(results)} sources",
                }
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Error scraping: {str(e)}"}
            )
    return JsonResponse({"success": False, "message": "Invalid request method"})
