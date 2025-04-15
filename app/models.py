from datetime import datetime, date
from typing import Optional, List
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), unique=True, nullable=False
    )
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), unique=True)
    role: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(20)
    )  # super_admin, vendor
    created_by: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("user.id"))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    last_login: so.Mapped[Optional[datetime]] = so.mapped_column(nullable=True)
    is_active: so.Mapped[bool] = so.mapped_column(default=True)

    # Relationships
    clients: so.WriteOnlyMapped["Client"] = so.relationship(back_populates="creator")
    payments: so.WriteOnlyMapped["Payment"] = so.relationship(back_populates="vendor")
    spendings: so.WriteOnlyMapped["Spending"] = so.relationship(back_populates="vendor")
    balances: so.WriteOnlyMapped["DailyBalance"] = so.relationship(
        back_populates="vendor"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"


# -------------------------
class Client(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
    status: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(30)
    )  # new, regular, inactive
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[Optional[datetime]] = so.mapped_column(
        onupdate=datetime.utcnow
    )

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    address_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("address.id"))

    creator: so.Mapped["User"] = so.relationship(back_populates="clients")
    phones: so.WriteOnlyMapped["ClientPhone"] = so.relationship(back_populates="client")
    address: so.Mapped[Optional["Address"]] = so.relationship()
    payments: so.WriteOnlyMapped["Payment"] = so.relationship(back_populates="client")


class ClientPhone(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    network: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    number: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False)

    client_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("client.id"), nullable=False
    )
    client: so.Mapped["Client"] = so.relationship(back_populates="phones")


class Address(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    street: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))
    city: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    gps_lat: so.Mapped[Optional[float]] = so.mapped_column()
    gps_lon: so.Mapped[Optional[float]] = so.mapped_column()
    territory: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))


class Payment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[float] = so.mapped_column(sa.Numeric(10, 2), nullable=False)
    network: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    payment_date: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    debt: so.Mapped[float] = so.mapped_column(sa.Numeric(10, 2), default=0)

    client_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("client.id"), nullable=False
    )
    vendor_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("user.id"), nullable=False
    )

    client: so.Mapped["Client"] = so.relationship(back_populates="payments")
    vendor: so.Mapped["User"] = so.relationship(back_populates="payments")


class Spending(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[float] = so.mapped_column(sa.Numeric(10, 2), nullable=False)
    purpose: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))
    recipient: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    spending_date: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    vendor_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("user.id"), nullable=False
    )
    vendor: so.Mapped["User"] = so.relationship(back_populates="spendings")


class DailyBalance(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    initial_sold: so.Mapped[Optional[float]] = so.mapped_column(sa.Numeric(10, 2))
    remaining_cash: so.Mapped[Optional[float]] = so.mapped_column(sa.Numeric(10, 2))

    vendor_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("user.id"), nullable=False
    )
    vendor: so.Mapped["User"] = so.relationship(back_populates="balances")
