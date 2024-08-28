from rest_framework.response import Response
from rest_framework.views import APIView

from main_app.serializers.v1 import cards
from main_app.permissions import StaffOnlyPermission
from .JWT import JWTAuthenticationAPIView
from utils.context import InContextAPI, CurrentContext
from utils.upload_files.parsers import LimitedMultiPartParser
from django.http import HttpResponseNotFound, HttpResponse

from main_app.models import Card, FederalSubject
from utils.pdf import CardPDF

from ajax_select import register, LookupChannel


class CreateCardAPIView(JWTAuthenticationAPIView):
    parser_classes = (LimitedMultiPartParser,)

    @InContextAPI()
    def post(self, request):
        ctx = CurrentContext()
        user = ctx.user
        if user.is_staff:
            serializer = cards.CreateCardForStuffSerializer(data=request.data)
        else:
            serializer = cards.CreateCardForUserSerializer(data=request.data)
        # raise serializer.errors
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()


class UpdateCardAPIView(JWTAuthenticationAPIView):
    permission_classes = (StaffOnlyPermission,)

    @InContextAPI()
    def post(self, request):
        serializer = cards.UpdateCardForStuffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()


class ShowCardAPIView(JWTAuthenticationAPIView):

    @InContextAPI()
    def post(self, request):
        serializer = cards.ShowCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)


class DownloadCardPDF(APIView):
    def get(self, request, card_uuid):
        try:

            card = Card.objects.get(card_uuid=card_uuid)
            if card.status != Card.SuccessChoice.SUCCESS:
                return HttpResponseNotFound()

        except Card.DoesNotExist:
            return HttpResponseNotFound()
        else:
            pdf = CardPDF(card)
            return HttpResponse(bytes(pdf.output()), content_type="application/pdf")


@register('subjects')
class FederalSubjectLookup(LookupChannel):

    model = FederalSubject

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:50]

    def format_item_display(self, item):
        return u"<span class='subject'>%s</span>" % item.name
