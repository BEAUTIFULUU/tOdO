class ListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lists = get_user_lists(user=request.user)

        return Response(lists)

    def put(self, request):
        lst = self.get(request)
        serializer = CreateListSerializer(lst, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)