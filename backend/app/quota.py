from datetime import datetime
from app.models import Usage, db

MAX_MONTHLY_QUOTA = 100
EXEMPT_TIERS = {"admin", "pro"}  # tiers that bypass quota enforcement

def check_monthly_quota(user_id, user_tier="free"):
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year

    usage = Usage.query.filter_by(user_id=user_id).first()

    if not usage:
        usage = Usage(
            user_id=user_id,
            count=1,
            last_reset=now,
            tier=user_tier
        )
        db.session.add(usage)
        db.session.commit()
        return True

    # Update tier if changed
    if usage.tier != user_tier:
        usage.tier = user_tier

    if usage.tier in EXEMPT_TIERS:
        return True

    # Reset if new month
    if usage.last_reset.month != current_month or usage.last_reset.year != current_year:
        usage.count = 1
        usage.last_reset = now
        db.session.commit()
        return True

    if usage.count >= MAX_MONTHLY_QUOTA:
        return False

    usage.count += 1
    db.session.commit()
    return True
