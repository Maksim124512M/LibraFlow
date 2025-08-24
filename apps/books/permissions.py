from rest_framework.permissions import BasePermission


class IsAdminOrLibrarian(BasePermission):
    '''
    Custom permission to only allow users with 'admin' or 'librarian' roles.
    '''

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in ('admin', 'librarian')