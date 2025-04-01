from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base
from connection import engine

# Base class for all models
Base = declarative_base()

# Hubs Table
class Hubs(Base):
    """
    Represents the 'hubs' table in the database.
    This table stores information about the distribution hubs.

    Columns:
    - hub_id: Primary key, unique identifier for each hub.
    - hub_name: Name of the hub.
    - hub_city: City where the hub is located.
    - hub_state: State where the hub is located.
    - hub_latitude: Latitude coordinate of the hub.
    - hub_longitude: Longitude coordinate of the hub.
    """
    __tablename__ = "hubs"
    __table_args__ = {'schema': 'public'}

    hub_id = Column(Integer, primary_key=True)
    hub_name = Column(String)
    hub_city = Column(String)
    hub_state = Column(String)
    hub_latitude = Column(Float)
    hub_longitude = Column(Float)

# Stores Table
class Stores(Base):
    """
    Represents the 'stores' table in the database.
    This table stores information about stores associated with hubs.

    Columns:
    - store_id: Primary key, unique identifier for each store.
    - hub_id: Foreign key linking to the 'hubs' table.
    - store_name: Name of the store.
    - store_segment: Segment/category of the store.
    - store_plan_price: Price associated with the store's plan.
    - store_latitude: Latitude coordinate of the store.
    - store_longitude: Longitude coordinate of the store.
    """
    __tablename__ = "stores"
    __table_args__ = {'schema': 'public'}

    store_id = Column(Integer, primary_key=True)
    hub_id = Column(Integer, ForeignKey("public.hubs.hub_id"))
    store_name = Column(String)
    store_segment = Column(String)
    store_plan_price = Column(Float)
    store_latitude = Column(Float)
    store_longitude = Column(Float)

# Channels Table
class Channels(Base):
    """
    Represents the 'channels' table in the database.
    This table stores information about communication channels.

    Columns:
    - channel_id: Primary key, unique identifier for each channel.
    - channel_name: Name of the channel.
    - channel_type: Type of the channel.
    """
    __tablename__ = "channels"
    __table_args__ = {'schema': 'public'}

    channel_id = Column(Integer, primary_key=True)
    channel_name = Column(String)
    channel_type = Column(String)

# Orders Table
class Orders(Base):
    """
    Represents the 'orders' table in the database.
    This table stores information about customer orders.

    Columns:
    - order_id: Primary key, unique identifier for each order.
    - store_id: Foreign key linking to the 'stores' table.
    - channel_id: Foreign key linking to the 'channels' table.
    - order_status: Status of the order (e.g., completed, pending).
    - order_amount: Total amount of the order.
    - order_delivery_fee: Fee for delivering the order.
    - order_delivery_cost: Cost for delivering the order.
    - order_created_hour, order_created_minute, order_created_day, order_created_month, order_created_year: Date and time components when the order was created.
    - order_moment_*: Timestamps indicating various stages of the order (e.g., created, accepted, ready, etc.).
    - order_metric_*: Various time metrics related to order processing (e.g., collection time, paused time, walking time, etc.).
    """
    __tablename__ = "orders"
    __table_args__ = {'schema': 'public'}

    order_id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("public.stores.store_id"))
    channel_id = Column(Integer, ForeignKey("public.channels.channel_id"))
    order_status = Column(String)
    order_amount = Column(Float)
    order_delivery_fee = Column(Float)
    order_delivery_cost = Column(Float)
    order_created_hour = Column(Integer)
    order_created_minute = Column(Integer)
    order_created_day = Column(Integer)
    order_created_month = Column(Integer)
    order_created_year = Column(Integer)
    order_moment_created = Column(TIMESTAMP)
    order_moment_accepted = Column(TIMESTAMP)
    order_moment_ready = Column(TIMESTAMP)
    order_moment_collected = Column(TIMESTAMP)
    order_moment_in_expedition = Column(TIMESTAMP)
    order_moment_delivering = Column(TIMESTAMP)
    order_moment_delivered = Column(TIMESTAMP)
    order_moment_finished = Column(TIMESTAMP)
    order_metric_collected_time = Column(Float)
    order_metric_paused_time = Column(Float)
    order_metric_production_time = Column(Float)
    order_metric_walking_time = Column(Float)
    order_metric_expediton_speed_time = Column(Float)
    order_metric_transit_time = Column(Float)
    order_metric_cycle_time = Column(Float)

# Payments Table
class Payments(Base):
    """
    Represents the 'payments' table in the database.
    This table stores payment information for orders.

    Columns:
    - payment_id: Primary key, unique identifier for each payment.
    - order_id: Foreign key linking to the 'orders' table.
    - payment_amount: Total amount of the payment.
    - payment_fee: Fee associated with the payment.
    - payment_method: Method used for the payment.
    - payment_status: Status of the payment.
    """
    __tablename__ = "payments"
    __table_args__ = {'schema': 'public'}

    payment_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("public.orders.order_id"))
    payment_amount = Column(Float)
    payment_fee = Column(Float)
    payment_method = Column(String)
    payment_status = Column(String)

# Drivers Table
class Drivers(Base):
    """
    Represents the 'drivers' table in the database.
    This table stores information about the drivers handling deliveries.

    Columns:
    - driver_id: Primary key, unique identifier for each driver.
    - driver_modal: Type of driver.
    - driver_type: Category of driver.
    """
    __tablename__ = "drivers"
    __table_args__ = {'schema': 'public'}

    driver_id = Column(Integer, primary_key=True)
    driver_modal = Column(String)
    driver_type = Column(String)

# Deliveries Table
class Deliveries(Base):
    """
    Represents the 'deliveries' table in the database.
    This table stores delivery-related information for orders.

    Columns:
    - delivery_id: Primary key, unique identifier for each delivery.
    - order_id: Foreign key linking to the 'orders' table.
    - driver_id: Foreign key linking to the 'drivers' table.
    - delivery_distance_meters: Distance covered by the delivery in meters.
    - delivery_status: Status of the delivery.
    """
    __tablename__ = "deliveries"
    __table_args__ = {'schema': 'public'}

    delivery_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("public.orders.order_id"))
    driver_id = Column(Integer, ForeignKey("public.drivers.driver_id"))
    delivery_distance_meters = Column(Float)
    delivery_status = Column(String)
