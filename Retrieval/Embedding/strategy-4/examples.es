GET _search
{
    "query": {
        "match_all": {}
    }
}

GET _cat/indices?v

//////////// Creating and Deleting Indices //////////////

PUT /sample_docs
{
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 2
    }
}

DELETE /sample_docs

//////////// Indexing Documents //////////////

PUT /sample_docs/_doc/20
{
    "product": "Tea Mug",
    "price": 10,
    "in_stock": 10
}

//////////// Retrieving Document by ID //////////////

GET /sample_docs/_doc/20

//////////// Updating Documents and Adding Fields //////////////

POST /sample_docs/_update/20
{
    "doc": {
        "in_stock": 20
    }
}

POST /sample_docs/_update/20
{
    "doc": {
        "branches": ["home", "kitchen"]
    }
}

//////////// Document Deletion //////////////

DELETE /sample_docs/_doc/20

//////////// More on Updates and Deletions //////////////

POST /sample_docs/_update/20
{
    "script": """
        if (ctx._source == 0) {
            ctx.op = 'noop'
        }
        ctx._source.in_stock--
        """
}

POST /sample_docs/_update_by_query
{
    "script": {
        "source": "ctx._source.in_stock --"
    },
    "query": {
        "match_all": {}
    }
}

//////////// Bulk API //////////////

POST _bulk
{ "index": { "_index": "test", "_id": 1 } }
{ "product": "Coffee Mug", "price": 10, "in_stock": 10 }
{ "delete": { "_index": "test", "_id": 2 } }
{ "create": { "_index": "test", "_id": 3 } }
{ "product": "Latte Mug", "price": 20, "in_stock": 30 }
{ "update": { "_index": "test", "_id": 1 } }
{ "doc": { "in_stock": 20 } }

//////////// Analyzer API //////////////

POST /_analyze
{
    "analyzer": "standard",
    "text": "Quick Brown Foxes"
}

POST /_analyze
{
    "text": "Quick Brown Foxes",
    "char_filter": [],
    "tokenizer": "standard",
    "filter": ["lowercase"]
}

//////////// Specifying a Custom Analyzer //////////////

PUT my-index
{
    "settings": {
        "analysis": {
            "analyzer": {
                "my_custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"]
                }
            },
            "filter": ["lowercase", "asciifolding"]
        }
    }
}

POST my-index/_analyze
{
    "analyzer": "my_custom_analyzer",
    "text": "Quick <b>Brown</b> Foxes"
}

////////////// A Short Note on Arrays //////////////

POST _analyze
{
    "text": ["This is", "a test", "of arrays"],
    "tokenizer": "standard"
}

////////////// Explicit Mapping //////////////

PUT /tweets
{
    "mappings": {
        "properties": {
            "tweet_text": {
                "type": "text"
            },
            "tweet_date": {
                "type": "date"
            },
            "author": {
                "properties":
                {
                    "first_name": {
                        "type": "text"
                    },
                    "last_name": {
                        "type": "text"
                    },
                    "email": {
                        "type": "keyword"
                    },
                    "age": {
                        "type": "integer"
                    }
                }
            },
            "user_id": {
                "type": "long"
            }
        }
    }
}

GET /tweets/_mapping

GET /tweets/_mapping/field/author.age

PUT /tweets/_doc/1
{
    "properties":{
        "likes": {
            "type": "integer"
        }
    }
}

////////////// Dates //////////////

GET /tweets/_search
{
    "query": {
        "range": {
            "tweet_date": {
                "gte": "2022-09-30T14:15:00Z",
                "lte": "2014-09-03"
            }
        }
    }
}

////////////// Re-Index //////////////

POST /_reindex
{
    "source": {
        "index": "tweets"
    },
    "dest": {
        "index": "tweets_new"
    }
}

////////////// Dynamic Mapping //////////////

POST /blog_posts/_doc/1
{
    "author.first_name": "John",
    "author.last_name": "Smith",
    "author.email": "",
    "blog_text": "Elasticsearch is great",
    "created_at": "2014-09-01",
    "rating": 3
}

GET /blog_posts/_mapping

////////////// Search //////////////

GET /tweets/_search?q=*

GET /tweets/_search?q=author.first_name:John

GET /tweets/_search
{
    "query": {
        "match_all": {}
    }
}

GET /tweets/_search
{
    "size": 10,
    "query": {
        "match_all": {},
    }
}

////////////// Term Level vs Full-Text Search Queries //////////////

GET products/_search
{
    "query": {
        "term": {
            "name": {
                "value": "coffee"
            }
        }
    }
}

GET products/_search
{
    "query": {
        "term": {
            "name": {
                "value": "Coffee"
            }
        }
    }
}

// Full-Text Search

GET products/_search
{
    "query": {
        "match": {
            "name": "coffee"
        }
    }
}


////////////// Term-Level Queries //////////////

GET /products/_search
{
    "_source":["name", "ins_stock", "tags"],
    "query":{
        "term": {
            "is_active": {
                "value": true
            }
        }
    }
}

// Search for Multiple Terms

GET /products/_search
{
    "query": {
        "terms": {
            "tags.keyword": ["Cake", "Coffee"]
        }
    }
}

GET /products/_search
{
    "query": {
        "ids": {
            "values": ["1", "2", "3"]
        }
    }
}

GET /products/_mapping

// Range Queries
GET /products/_search
{
    "query": {
        "range": {
            "price": {
                "gte": 10,
                "lte": 20
            }
        }
    }
}

GET /products/_search
{
    "query":{
        "range": {
            "created": {
                "gte": "2014-09-01",
                "lte": "2014-09-03"
            }
        }
    }
}

////////////// Check for Existing Fields //////////////

GET /products/_search
{
    "query": {
        "exists": {
            "field": "tags"
        }
    }
}

////////////// Prefix Queries and Regular Expressions //////////////

GET /products/_search
{
    "query": {
        "prefix": {
            "tags.keyword": "Vege"
        }
    }
}

GET /products/_search
{
    "query": {
        "regexp": {
            "tags.keyword": "Vege.*"
        }
    }
}

////////////// Full-Text Queries //////////////

GET /recipes/_search
{
    "query": {
        "match": {
            "title": "Pasta Carbonara",
            "operator": "and"
        }
    }
}

// Phrase Queries

GET /recipes/_search
{
    "query": {
        "match_phrase": {
            "title": "Pasta Carbonara"
        }
    }
}

GET /recipes/_search
{
    "query": {
        "match_phrase": {
            "title": {
                "query": "Pasta Carbonara",
                "slop": 1
            }
        }
    }
}

// Multi-Match Queries

GET /recipes/_search
{
    "query": {
        "multi_match": {
            "query": "Pasta Carbonara",
            "fields": ["title", "description"]
        }
    }
}

// Boolean Queries

GET /recipes/_search
{
    "query": {
        "bool": {
            "must": {
                "match": {
                    "title": "Pasta Carbonara"
                }
            },
            "filter": {
                "range": {
                    "created": {
                        "gte": "2014-09-01",
                        "lte": "2014-09-03"
                    }
                }
            }
        }
    }
}

/////////////////////////////////////

PUT /med_e5_recursivechar
{
    "settings": {
        "index": {
            "refresh_interval": -1,
            "knn": true,
            "knn.algo_param.ef_search": 512
        }
    }
}