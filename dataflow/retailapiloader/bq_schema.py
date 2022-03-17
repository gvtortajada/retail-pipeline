def retail_schema():
    return {
    'fields':[
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "type",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "primaryProductId",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "collectionMemberIds",
    "type": "STRING",
    "mode": "REPEATED"
  },
  {
    "name": "gtin",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "categories",
    "type": "STRING",
    "mode": "REPEATED"
  },
  {
    "name": "title",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "brands",
    "type": "STRING",
    "mode": "REPEATED"
  },
  {
    "name": "description",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "languageCode",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "attributes",
    "type": "RECORD",
    "mode": "REPEATED",
    "fields": [
      {
        "name": "key",
        "type": "STRING",
        "mode": "NULLABLE"
      },
      {
        "name": "value",
        "type": "RECORD",
        "mode": "NULLABLE",
        "fields": [
          {
            "name": "text",
            "type": "STRING",
            "mode": "REPEATED"
          },
          {
            "name": "numbers",
            "type": "FLOAT",
            "mode": "REPEATED"
          },
          {
            "name": "searchable",
            "type": "BOOLEAN",
            "mode": "NULLABLE"
          },
          {
            "name": "indexable",
            "type": "BOOLEAN",
            "mode": "NULLABLE"
          }
        ]
      }
    ]
  },
  {
    "name": "tags",
    "type": "STRING",
    "mode": "REPEATED"
  },
  {
    "name": "priceInfo",
    "type": "RECORD",
    "mode": "NULLABLE",
    "fields": [
      {
        "name": "currencyCode",
        "type": "STRING",
        "mode": "NULLABLE"
      },
      {
        "name": "price",
        "type": "FLOAT",
        "mode": "NULLABLE"
      },
      {
        "name": "originalPrice",
        "type": "FLOAT",
        "mode": "NULLABLE"
      },
      {
        "name": "cost",
        "type": "FLOAT",
        "mode": "NULLABLE"
      },
      {
        "name": "priceEffectiveTime",
        "type": "STRING",
        "mode": "NULLABLE"
      },
      {
        "name": "priceExpireTime",
        "type": "STRING",
        "mode": "NULLABLE"
      }
    ]
  },
  {
    "name": "rating",
    "type": "RECORD",
    "mode": "NULLABLE",
    "fields": [
      {
        "name": "ratingCount",
        "type": "INTEGER",
        "mode": "NULLABLE"
      },
      {
        "name": "averageRating",
        "type": "FLOAT",
        "mode": "NULLABLE"
      },
      {
        "name": "ratingHistogram",
        "type": "INTEGER",
        "mode": "REPEATED"
      }
    ]
  },
  {
    "name": "expireTime",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "ttl",
    "type": "RECORD",
    "mode": "NULLABLE",
    "fields": [
      {
        "name": "seconds",
        "type": "INTEGER",
        "mode": "NULLABLE"
      },
      {
        "name": "nanos",
        "type": "INTEGER",
        "mode": "NULLABLE"
      }
    ]
  },
  {
    "name": "availableTime",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "availability",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "availableQuantity",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "fulfillmentInfo",
    "type": "RECORD",
    "mode": "REPEATED",
    "fields": [
      {
        "name": "type",
        "type": "STRING",
        "mode": "NULLABLE"
      },
      {
        "name": "placeIds",
        "type": "STRING",
        "mode": "REPEATED"
      }
    ]
  },
  {
    "name": "uri",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "images",
    "type": "RECORD",
    "mode": "REPEATED",
    "fields": [
      {
        "name": "uri",
        "type": "STRING",
        "mode": "REQUIRED"
      },
      {
        "name": "height",
        "type": "INTEGER",
        "mode": "NULLABLE"
      },
      {
        "name": "width",
        "type": "INTEGER",
        "mode": "NULLABLE"
      }
    ]
  },
  {
    "name": "audience",
    "type": "RECORD",
    "mode": "NULLABLE",
    "fields": [
      {
        "name": "genders",
        "type": "STRING",
        "mode": "REPEATED"
      },
      {
        "name": "ageGroups",
        "type": "STRING",
        "mode": "REPEATED"
      }
    ]
  },
  {
    "name": "colorInfo",
    "type": "RECORD",
    "mode": "NULLABLE",
    "fields": [
      {
        "name": "colorFamilies",
        "type": "STRING",
        "mode": "REPEATED"
      },
      {
        "name": "colors",
        "type": "STRING",
        "mode": "REPEATED"
      }
    ]
  },
  {
    "name": "sizes",
    "type": "STRING",
    "mode": "REPEATED"
  },
  {
    "name": "materials",
    "type": "STRING",
    "mode": "REPEATED"
  },
  {
    "name": "patterns",
    "type": "STRING",
    "mode": "REPEATED"
  },
  {
    "name": "conditions",
    "type": "STRING",
    "mode": "REPEATED"
  },
  {
    "name": "retrievableFields",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "publishTime",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "promotions",
    "type": "RECORD",
    "mode": "REPEATED",
    "fields": [
      {
        "name": "promotionId",
        "type": "STRING",
        "mode": "NULLABLE"
      }
    ]
  }
]
}