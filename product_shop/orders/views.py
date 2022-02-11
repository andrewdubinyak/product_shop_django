import json

from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product_shop.orders.models import Order
from product_shop.orders.serializers import OrderSerializer
from product_shop.services.order_service import get_total_cart_price
from product_shop.services.redis_service import add_to_cart, remove_from_cart, get_all_cart


class CartView(views.APIView):

    @staticmethod
    def get(request):
        session_key = request.session.session_key
        if not session_key:
            request.session['session_key'] = 'cart'
        else:
            cart_items = get_all_cart(session_key)
            if not cart_items:
                return Response({'message': 'cart is empty'})
            else:
                response = {
                    'total_price': get_total_cart_price(cart_items),
                    'cart': cart_items
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response({'message': 'cart is empty'})

    @staticmethod
    def post(request):
        session_key = request.session.session_key
        request.session['session_key'] = 'cart'
        if not session_key:
            request.session['session_key'] = 'cart'
            session_key = request.session.session_key

        data = json.loads(request.body)
        add_to_cart(session_key, data)

        response = {
            'message': f"product_{data['product_id']} successfully added to cart"
        }
        return Response(response, 201)

    @staticmethod
    def delete(request, **product_id):
        session_key = request.session.session_key
        product_id = product_id.get('id')
        remove_from_cart(session_key, product_id)
        return Response({'message': f'product_{product_id} successfully deleted'})


class OrderView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        serializer = OrderSerializer(
            data=request.data,
            context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request, **order_id):
        order_id = order_id.get('id')
        courier = 1
        if order_id:
            order = Order.objects.filter(id=order_id)
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if request.user.user_type == courier:
                orders = Order.objects.filter(courier=request.user).all()
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                orders = Order.objects.filter(customer=request.user).all()
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


class OrderAssignView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, **order_id):
        order_id = order_id.get('id')
        order = Order.objects.filter(id=order_id, courier=None).first()
        if order:
            order.courier = request.user
            order.save()
        else:
            return Response({'message': 'Order not found!'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Orders Successfully assigned'}, status=status.HTTP_200_OK)
