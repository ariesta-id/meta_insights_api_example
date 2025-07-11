# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "facebook-business",
#     "python-dotenv",
# ]
# ///
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError


def contact_api(
    fields,
    params,
    aaid,
):
    api_response = AdAccount(ACT_ + aaid).get_insights(
        fields=fields,
        params=params,
    )
    return api_response[0]


def set_params(
    date_since: str,
    date_until: str,
    filtering: list[dict] = [],
    level: str = "account",
    time: str = "all_days",
):
    # iTODO: f filtering [], archived & deleted, included https://developers.facebook.com/docs/marketing-api/insights/
 
    # Check if date_since & date_until is a valid date string with "%Y-%m-%d" formatting
    try:
        date_since_date = datetime.strptime(date_since, "%Y-%m-%d")
        date_until_date = datetime.strptime(date_until, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

    # Check if date_until_date >= date_since_date, raise Error if not
    if date_until_date < date_since_date:
        raise ValueError(
            "date_until_date should be greater than or equal to date_since_date"
        )

    return {
        "time_range": {"since": date_since, "until": date_until},
        "filtering": filtering,
        "level": level,
        "breakdowns": [],
        "time_increment": time,
        "use_unified_attribution_setting": True,
        "app_id": APP_ID,
        "app_secret": APP_SECRET,
    }

if __name__ == "__main__":

    load_dotenv()

    AD_ACCOUNT_ID = "(your ad account id)"  # For trying, fill this
    ACT_ = "act_"
    APP_ID = os.getenv("META_APP_ID")
    APP_SECRET = os.getenv("META_APP_SECRET ")
    META_TOKEN = os.getenv("META_API_ACCESS_TOKEN")
    FacebookAdsApi.init(access_token=META_TOKEN, api_version="v20.0")

    params = set_params(
        date_since="2025-07-06",
        date_until="2025-07-06",
    )

    try:
        print(contact_api(["spend"], params, AD_ACCOUNT_ID))
    except FacebookRequestError as e:
        print(str(e))
