from agro_db.delivery.models import PaymentMode
from lastmiledelivery.conf.environment.client_setup import ClientsFactory
from lastmiledelivery.utils.unicommerce.unicommerce_pull_utils import get_unicommerce_client
from lastmiledelivery.utils.config_utils import get_env_config

def init_variables(app):
    if not app:
        raise Exception
    try:
        all_payment_modes = PaymentMode.objects.all()
        app.cash_mode = PaymentMode.objects.get(lable__icontains='CASH')
        app.payment_modes = dict()
        for payment_mode in all_payment_modes:
            app.payment_modes[payment_mode.uuid] = payment_mode
    except:
        print "failed to init locals cash_mode and card_mode"
    app.auth_header_name = 'X-Authorization-Token'
    app.facility_cookie_name = 'facility'
    app.facility_header_name = 'facility'
    app.quick_cash_wallet_type = 'QCW'
    app.postpaid_incentive_wallet_type = 'PPI'
    app.field_easy_api_key = "fbabc540-c1f9-4d59-92da-d33b2510dc02"
    app.field_easy_api_token = "cae8c956-9800-4a81-aa25-042b5916aaeb"
    app.is_field_eazy_active = True
    config = get_env_config()
    uni_url = config.UNICOMMERCE_URL
    uni_token = config.UNICOMMERCE_TOKEN
    app.unicommerce_client = ClientsFactory(app).get_unicommerce_client()
    return
