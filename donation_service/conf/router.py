from lastmiledelivery.controllers.ping import Ping
from lastmiledelivery.controllers.manifest import Manifest
from lastmiledelivery.controllers.lp_payment import PostPaidPayment
from lastmiledelivery.controllers.quick_cash import QuickCash
from lastmiledelivery.controllers.out_going_payment import OutGoingPayment
from lastmiledelivery.controllers.lp_incentive import LPIncentive
from lastmiledelivery.controllers.transaction_method import TransactionMethod
from lastmiledelivery.controllers.user_validation import UserValidation
from lastmiledelivery.controllers.franchise import Franchise
from lastmiledelivery.controllers.pickup_location import PickupLocation
from lastmiledelivery.controllers.location import Location
from lastmiledelivery.controllers.warehouse_executive import WarehouseExecutive
from lastmiledelivery.controllers.return_manifest import ReturnManifest
from lastmiledelivery.controllers.agrostar_account import AgroStarAccount
from lastmiledelivery.controllers.transport_location import TransportLocation
from lastmiledelivery.controllers.transport import Transport
from lastmiledelivery.controllers.channel import Channel
from lastmiledelivery.controllers.packages import Packages
from lastmiledelivery.controllers.package import Package
from lastmiledelivery.controllers.firebase_token import FirebaseToken
from lastmiledelivery.controllers.return_request import ReturnRequest
from lastmiledelivery.controllers.return_request_action import \
    ReturnRequestAction
from lastmiledelivery.controllers.package_status import PackageStatus
from lastmiledelivery.controllers.lead_generation import Lead
from lastmiledelivery.controllers.version import Version
from lastmiledelivery.controllers.auto_reconciliate import AutoReconciliate
from lastmiledelivery.controllers.package_reassignment import PackageReassignment



def setup_routing(api):
    api.add_resource(Ping, "ping/")
    api.add_resource(Manifest, "manifest/<string:manifest_id>/",
                     "manifest/")
    api.add_resource(UserValidation, "uservalidation/")
    api.add_resource(Franchise, "franchise/",
                     "franchise/<string:franchise_id>/")
    api.add_resource(WarehouseExecutive, "executive/",
                     "executive/<string:executive_id>/")
    api.add_resource(ReturnManifest, "returnmanifest/",
                     "returnmanifest/<string:return_manifest_id>/")
    api.add_resource(PickupLocation, "pickuplocation/",
                     "pickuplocation/<int:address_id>/")
    api.add_resource(TransportLocation, "transportlocation/",
                     "transportlocation/<string:transport_location_id>/")
    api.add_resource(Location, 'location/')
    api.add_resource(AgroStarAccount, "agrostaraccounts/",
                     "agrostaraccounts/<string:account_id>/")
    api.add_resource(Transport, "transport/",
                     "transport/<string:transport_id>/")
    api.add_resource(PostPaidPayment, "lppayment/",
                     "lppayment/<int:payment_id>/")
    api.add_resource(OutGoingPayment, "outgoingpayment/",
                     "outgoingpayment/<int:payout_id>/")
    api.add_resource(LPIncentive, "incentive/",
                     "incentive/<int:payout_id>/")
    api.add_resource(QuickCash, "quickcash/",
                     "quickcash/<int:quickcash_id>")
    api.add_resource(TransactionMethod, "transactionmethods/",
                     "transactionmethods/<int:method_id>/")
    api.add_resource(Channel, "channel/")
    api.add_resource(Packages, "packages/",
                     "packages/<string:code>/")
    api.add_resource(Package, "package/")
    api.add_resource(FirebaseToken, "fcm/")
    api.add_resource(ReturnRequest, "returnrequest/",
                     "returnrequest/<int:request_id>/")
    api.add_resource(ReturnRequestAction, "returnrequest/action/")
    api.add_resource(AutoReconciliate,
                     "franchise/<string:franchise_id>/autoreconciliate/")
    api.add_resource(Lead,"lead/")
    api.add_resource(PackageStatus, "packagestatusedit/<string:package_id>/")
    api.add_resource(Version, "version/", "version/<string:version_id>/")
    api.add_resource(PackageReassignment,  "packagereassignment/")
    return
