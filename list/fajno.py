class ListView(APIView, PageNumberPagination):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

    def get(self, request):
        lists = get_user_lists(user=request.user)
        paginated_data = self.paginate_queryset(lists, request, view=self)
        serializer = ListSerializer(paginated_data, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CreateUpdateListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)


class ListDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, list_id):
        ls_details = get_list_details(list_id=list_id)
        serializer = ListDetailSerializer(ls_details)
        return Response(serializer.data)

    def put(self, request, list_id):
        validated_data = validate_list_data(request.data)
        updated_list = update_list(list_id=list_id, user=request.user, data=validated_data)
        serializer = CreateUpdateListSerializer(updated_list)
        return Response(serializer.data)

    def delete(self, request, list_id):
        delete_list(list_id=list_id, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskView(APIView, PageNumberPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, list_id):
        tasks = get_list_tasks(list_id=list_id)
        paginated_data = self.paginate_queryset(tasks, request, view=self)
        serializer = TaskSerializer(paginated_data, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, list_id):
        serializer = CreateUpdateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(list_id=list_id)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, list_id, task_id):
        task_details = get_task_details(task_id=task_id, list_id=list_id)
        serializer = TaskSerializer(task_details)
        return Response(serializer.data)

    def put(self, request, list_id, task_id):
        validated_data = validate_task_data(data=request.data)
        updated_task = update_task(task_id=task_id, list_id=list_id, data=validated_data, user=request.user)
        serializer = CreateUpdateTaskSerializer(updated_task)
        return Response(serializer.data)

    def delete(self, request, task_id, list_id):
        delete_task(task_id=task_id, list_id=list_id)
        return Response(status=status.HTTP_204_NO_CONTENT)