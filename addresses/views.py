from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Address
from .utils import PropertyURLFinder


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
        state_input = request.POST.get("state", "").strip()
        if address_input:
            # Parse the input: support "street, suburb", "street\tsuburb", or "street suburb"
            if "," in address_input:
                parts = address_input.split(",", 1)  # split on first comma
                street = parts[0].strip()
                suburb = parts[1].strip() if len(parts) > 1 else ""
            elif "\t" in address_input:
                parts = [part.strip() for part in address_input.split("\t") if part.strip()]
                street = parts[0] if len(parts) > 0 else ""
                suburb = parts[1] if len(parts) > 1 else ""
                if not state_input and len(parts) > 2:
                    state_input = parts[2]
            else:
                # Fallback: split by last space
                last_space = address_input.rfind(" ")
                if last_space > 0:
                    street = address_input[:last_space].strip()
                    suburb = address_input[last_space:].strip()
                else:
                    street = address_input
                    suburb = ""
            if street:
                # Use provided state or parsed suburb if it looks like a state
                state = state_input or ""
                if not state and suburb:
                    # Check if suburb ends with a state abbreviation
                    suburb_upper = suburb.upper()
                    if suburb_upper.endswith(
                        (" NSW", " VIC", " QLD", " WA", " SA", " TAS", " ACT", " NT")
                    ):
                        parts = suburb.rsplit(" ", 1)
                        suburb = parts[0]
                        state = parts[1]
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


@require_POST
def find_property_urls(request, pk):
    """AJAX endpoint to find property URLs for an address."""
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Authentication required", "diagnostics": {}},
            status=401,
        )

    addr = get_object_or_404(Address, pk=pk)

    # Create full address string for searching
    full_address = f"{addr.street_address}, {addr.suburb}"
    if addr.state:
        full_address += f", {addr.state}"

    finder = PropertyURLFinder()
    result = finder.find_property_urls(full_address)
    found_urls = result.get("urls", [])
    diagnostics = result.get("diagnostics", {})

    return JsonResponse(
        {
            "address": full_address,
            "found_urls": found_urls,
            "count": len(found_urls),
            "diagnostics": diagnostics,
        }
    )


@require_POST
@login_required
def address_delete(request, pk):
    """Delete an address."""
    addr = get_object_or_404(Address, pk=pk)
    addr.delete()
    return redirect(reverse("address_list"))
