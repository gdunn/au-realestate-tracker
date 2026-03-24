from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Address


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
            # Parse the input: support "street, suburb", "street\tsuburb", or "street suburb"
            if "," in address_input:
                parts = address_input.split(",", 1)  # split on first comma
                street = parts[0].strip()
                suburb = parts[1].strip() if len(parts) > 1 else ""
            elif "\t" in address_input:
                parts = address_input.split("\t", 1)
                street = parts[0].strip()
                suburb = parts[1].strip() if len(parts) > 1 else ""
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
                Address.objects.create(street_address=street, suburb=suburb)
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
