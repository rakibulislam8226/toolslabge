from django.db.models import Q


def get_fullname_query(search_term, user_fields_prefix="user"):
    """
    Build a Q object for flexible full name search across first_name and last_name.
    Supports multi-word search (e.g., "rakib islam").
    """
    if not search_term:
        return Q()

    terms = search_term.strip().split()
    q = Q()

    for term in terms:
        q |= Q(**{f"{user_fields_prefix}__first_name__icontains": term}) | Q(
            **{f"{user_fields_prefix}__last_name__icontains": term}
        )

    return q
