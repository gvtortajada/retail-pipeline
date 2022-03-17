from typing import List, Optional
from dataclasses import dataclass

@dataclass
class AttributeValue:
    text: List[str]
    numbers: List[float]
    searchable: Optional[bool]
    indexable: Optional[bool]


@dataclass
class Attribute:
    key: Optional[str]
    value: Optional[AttributeValue]


@dataclass
class PriceInfo:
    currencyCode: Optional[str]
    price: Optional[float]
    originalPrice: Optional[float]
    cost: Optional[float]
    priceEffectiveTime: Optional[str]
    priceExpireTime: Optional[str]


@dataclass
class Rating:
    seconds: Optional[int]
    nanos: Optional[float]


@dataclass
class Ttl:
    ratingCount: Optional[int]
    averageRating: Optional[float]
    ratingHistogram: Optional[int]


@dataclass
class FulfillmentInfo:
    type: Optional[str]
    placeIds: List[str]


@dataclass
class Image:
    uri: str
    height: Optional[int]
    width: Optional[int]


@dataclass
class Audience:
    genders: List[str]
    ageGroups: List[str]


@dataclass
class ColorInfo:
    colorFamilies: List[str]
    colors: List[str]


@dataclass
class Promotion:
    promotionId: Optional[str]


@dataclass(init=False)
class Product:
    """
        GCP Retail product based on retail product catalog schema:
        https://cloud.google.com/retail/docs/catalog#expandable-1
    """
    name: Optional[str]
    id: str
    type: Optional[str]
    primaryProductId: Optional[str]
    collectionMemberIds: List[str]
    gtin: Optional[str]
    categories: List[str]
    title: str
    brands: List[str]
    description: Optional[str]
    languageCode: Optional[str]
    attributes: List[Attribute]
    tags: List[str]
    priceInfo: Optional[PriceInfo]
    rating: Optional[Rating]
    expireTime: Optional[str]
    ttl: Optional[Ttl]
    availableTime: Optional[str]
    availability: Optional[str]
    availableQuantity: Optional[int]
    fulfillmentInfo: List[FulfillmentInfo]
    uri: Optional[str]
    images: List[Image]
    audience: Optional[Audience]
    sizes: List[str]
    materials: List[str]
    patterns: List[str]
    conditions: List[str]
    retrievableFields: Optional[str]
    publishTime: Optional[str]
    promotions: List[Promotion]