from django.shortcuts import render

from .models import Address

# simple list view for addresses; sorting is controlled via the ``sort``
# query parameter, which currently supports ``date`` (default) and ``suburb``.
#
# - ``date`` sorts by the time the record was entered (newest first).
# - ``suburb`` sorts alphabetically by suburb.
#
# A template at ``addresses/address_list.html`` is expected to render the
# results.


def address_list(request):
    sort = request.GET.get("sort")
    if sort == "suburb":
        addresses = Address.objects.order_by("suburb")
    else:
        # default to date; show newest first
        addresses = Address.objects.order_by("-created_at")

    return render(request, "addresses/address_list.html", {"addresses": addresses})
