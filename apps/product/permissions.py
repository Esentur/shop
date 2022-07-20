from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomIsAdmin(BasePermission):
    # create(POST) list(GET) (где не нужен id)
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated and request.user.is_staff

    # update delete retrieve (где нужен id)
    def has_object_permission(self, request, view, obj):
        # print(SAFE_METHODS)
        # print(obj)
        # print(request.user)
        if request.method in SAFE_METHODS:# если незареганный отправить GET(retrieve) запрос, то можно
            return True
        return request.user.is_authenticated and request.user.is_staff
