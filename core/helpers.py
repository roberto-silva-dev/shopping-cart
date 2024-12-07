from rest_framework.response import Response
from rest_framework import status


def return_list_api(self):
    try:
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        return Response({'results': serializer_class(queryset, many=True, context={'request': self.request}).data})
    except Exception as e:
        print(e)
        return Response({'message': "Something went wrong on the server!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

