# Solr Guide

## System Requirements

Java >1.8

## Directory layout

### bin/

Control scripts

* #### solr and solr.cmd

  `bin/solr` on *nix, `bin/solr.cmd` on Windows. Use to create collections/cores, configuration

* #### post

  POSTing content to Solr

* #### solr.in.sh and solr.in.cmd

  Property files for Java, Jetty, and Solr

* #### install_solr_service.sh

  To install Solr as a service on *nix 

### contrib/

Plugins

### dist/

Main `.jar` files

### server/

* Solr Admin UI: `server/solr-webapp`
* Jetty libs: `server/lib`
* Logs and log config (`server/resources`)
* Sample configsets: `server/solr/configsets`

<hr/>

## Control Script Reference

### Start Solr

```bash
bin/solr start
```

#### Options:

`-cloud`: 	Start in Cloud mode

`-f`:	Start in foreground

`-h <hostname>`: Start with defined hostname

`-p <port>`: Start with defined port number

`-s <dir>`: Set Solr home directory. Defaults to `server/solr`. Cores are created under this directory. Usually set when multiple Solr instances run on same host. If set, the directory should contain a `solr.xml` file.

### Stop Solr

#### On a particular port

```bash
bin/solr stop -p <port>
```

#### All running instances

```bash
bin/solr stop -all
```



### Restart Solr

```bash
bin/solr restart
```

### Check status

```bash
bin/solr status
```

### Create new core

```bash
bin/solr create -c <name>
```

#### Options

`-d <confdir>`

Configuration directory. If not specified, it will use `_default` configset directory. In SolrCloud mode, this will be uploaded as a copy to ZooKeeper.

`-p <port>`

`-s <shards`

Number of shards to split the collection into (in Solr Cloud mode only)

`-rf <replicas>`

Number of replicas

### Delete Core

```bash
bin/solr delete -c <name>
```

## Admin UI

```
http://localhost:8983/solr/
```

<hr/>

## Configuration files

### Solr Home

* By default, it's `server/solr`.
* Solr stores it's index here.
* As well as important configurations
* Layout different in standalone and cloud mode

**Standalone**

```
<solr-home-directory>/
   solr.xml
   core_name1/
      core.properties
      conf/
         solrconfig.xml
         managed-schema
      data/
   core_name2/
      core.properties
      conf/
         solrconfig.xml
         managed-schema
      data/
```

**SolrCloud**

```
<solr-home-directory>/
   solr.xml
   core_name1/
      core.properties
      data/
   core_name2/
      core.properties
      data/
```

#### Config files

* `solr.xml`: config for Solr server instance

* Per Solr Core

  | File                            | Purpose                                                      |
  | ------------------------------- | ------------------------------------------------------------ |
  | `core.properties`               | Properties for each core, collection it belongs to, schema location, etc. |
  | `solrconfig.xml`                | High-level behaviour                                         |
  | `managed-schema` / `schema.xml` | Describes documents which will be indexed                    |
  | `data/`                         | Low-level index files                                        |
  
* In **SolrCloud**, there's no `conf` directory per-core. The configuration files are stored in ZooKeeper.

### Export configuration files from SolrCloud deployment (Download from ZooKeeper)

Refer to: https://www.searchstax.com/docs/hc/copy-solr-config/

```bash
./zkcli.sh -zkhost <zookeeper URL> -cmd downconfig -confdir <local directory> -confname <config name>
```



<hr/>

## Schema and Documents

### Accesing and editing schema

* `managed-schema`: Used to make schema changes at runtime or via Schema API, or in Schemaless Mode
* `schema.xml`: The traditional schema file that can be edited manually
* SolrCloud: neither of these maybe available. Instead, access through Schema API or Admin UI's Cloud Screens

### Field Types

Field type definition includes:

* Name
* Implementation class
* For `TextField`, description of field analysis
* Field type properties

**Example:** (in `schema.xml`)

```xml
<fieldType name="text_general" class="solr.TextField" positionIncrementGap="100"> 
  <analyzer type="index"> 
    <tokenizer class="solr.StandardTokenizerFactory"/>
    <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
    <!-- in this example, we will only use synonyms at query time
    <filter class="solr.SynonymFilterFactory" synonyms="index_synonyms.txt" ignoreCase="true" expand="false"/>
    -->
    <filter class="solr.LowerCaseFilterFactory"/>
  </analyzer>
  <analyzer type="query">
    <tokenizer class="solr.StandardTokenizerFactory"/>
    <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
    <filter class="solr.SynonymFilterFactory" synonyms="synonyms.txt" ignoreCase="true" expand="true"/>
    <filter class="solr.LowerCaseFilterFactory"/>
  </analyzer>
</fieldType>
```

#### Field Type Properties

##### General

| Property                    | Purpose                                                      |
| --------------------------- | ------------------------------------------------------------ |
| `name`                      | Field type name                                              |
| `class`                     | Implementing class                                           |
| `positionIncrementGap`      | For multivalued fields, distance between multiple values (avoid accidentally matching phrases across values) |
| `autoGeneratePhraseQueries` | Auto generate phrase queries for adjacent terms.             |

##### Default

| Property       | Description                                                  | Default value |
| -------------- | ------------------------------------------------------------ | ------------- |
| `indexed`      | Field can be used in queries to match documents              | `true`        |
| `stored`       | The value itself can be *retrieved* by queries               | `true`        |
| `multiValued`  | Single document may contain multiple values for this field type. E.g. many food items in a menu. | `false`       |
| `required`     | Solr will reject an attempt to index document that doesn't have this field. | `false`       |
| `uninvertible` | If `true`, means it **can** be inverted. Default `true`, but should be set to `false` with `docValues=true` for stability. | `true`        |
| `docValues`    | Field in DocValues structure.                                | `false`       |

#### Included Field Types

| Class              | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `BoolField`        | True: `1`, `t`, `T`. <br />Any other value false             |
| `CollationField`   | Unicode collation for sorting and range queries.             |
| `DateRangeField`   | Including point in time date instances down to single-millisecond durations |
| `DatePointField`   | Point in time with ms precision                              |
| `DoublePointField` | 64-bit float                                                 |
| `FloatPointField`  | 32-bit float                                                 |
| `IntPointField`    | 32-bit signed int                                            |
| `StrField`         | Short strings that are not tokenized or analysed             |
| `TextField`        | Text with multiple words or tokens. Only text fields, usually, have analysers. |

##### Dates

Format:

```
YYYY_MM_DDThh:mm:ssZ
```

`T` is separator between date and time.

`Z` is literally 'Z' to indicate UTC. No timezone can be specified.

### Copying Fields

Copy one or more fields to another field. Copy happens **before** analysis, so can apply different analyser chain on same data.

E.g for single field.

```xml
<copyField source="cat" dest="text" maxChars="30000" />
```

If receiving copied fields from multiple fields into one, the destination field must be `multivalued="true"`.

### Unique Key

Define unique key by:

```xml
<uniqueKey>id</uniqueKey>
```

### Schema API

POST to:

```
/api/<collections|cores>/<name>/schema/
```

Commands:

| Commands            | Description |
| ------------------- | ----------- |
| `add-field`         |             |
| `delete-field`      |             |
| `replace-field`     |             |
| `add-copy-field`    |             |
| `delete-copy-field` |             |

E.g.

```bash
curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"sell_by",
     "type":"pdate",
     "stored":true }
}' http://localhost:8983/api/collections/gettingstarted/schema
```

<hr/>

## Analyzers, Tokenizers, Filters

* Field analyzers - during ingest and at query time. Examines text and createas a token stream. Composed of a single class or a series of:
  * Tokenizersr
  * Filters

### Analyzers

Only for `TextField` and `SortableTextField` usually.

Specified as child of `fieldType`

Example of single-class analayzer:

```xml
<fieldType name="nametext" class="solr.TextField">
  <analyzer class="org.apache.lucene.analysis.core.WhitespaceAnalyzer"/>
</fieldType>
```

Chained analyzer:

```xml
<fieldType name="nametext" class="solr.TextField">
  <analyzer>
    <tokenizer class="solr.StandardTokenizerFactory"/>
    <filter class="solr.LowerCaseFilterFactory"/>
    <filter class="solr.StopFilterFactory"/>
    <filter class="solr.EnglishPorterFilterFactory"/>
  </analyzer>
</fieldType>
```

#### Analyzer Phases

The above analyzers would apply for both ingest and query time. However, we can specify when they are applicable, with `type` param on analyzer. E.g.:

```xml
<fieldType name="nametext" class="solr.TextField">
  <analyzer type="index">
    <tokenizer class="solr.StandardTokenizerFactory"/>
    <filter class="solr.LowerCaseFilterFactory"/>
    <filter class="solr.KeepWordFilterFactory" words="keepwords.txt"/>
    <filter class="solr.SynonymFilterFactory" synonyms="syns.txt"/>
  </analyzer>
  <analyzer type="query">
    <tokenizer class="solr.StandardTokenizerFactory"/>
    <filter class="solr.LowerCaseFilterFactory"/>
  </analyzer>
</fieldType>
```

### Important tokenizers
#### N-Gram and Edge N-Gram Tokenizer Factories
```xml
<tokenizer class="solr.NGramTokenizerFactory" minGramSize="4" maxGramSize="5"/>
```
```xml
<tokenizer class="solr.EdgeNGramTokenizerFactory"/>
```

Break up tokens (e.g. individual words) into smaller tokens, either from any part of the token or from the edges only.

Neccessary for partial matches, e.g. 'pizz' matching 'pizza'.

<hr/>

## Indexing

Three methods most commonly used

* Using Solr Cell built on Apache Tika to ingest binary data
* Upload XML files by sending HTTP requests
* Custom Java application that uses Solr client API

### POST tool

Shell script.

```bash
bin/post -c <collection name> <filename>
```

### XML index updates

`<add>`: documents are being added

`<doc>`: encapsulate the document itself

`<field>`: the content for specific fields.

E.g:

```xml
<add>
  <doc>
    <field name="authors">Patrick Eagar</field>
    <field name="subject">Sports</field>
    <field name="dd">796.35</field>
    <field name="numpages">128</field>
    <field name="desc"></field>
    <field name="price">12.40</field>
    <field name="title">Summer of the all-rounder: Test and championship cricket in England 1982</field>
    <field name="isbn">0002166313</field>
    <field name="yearpub">1982</field>
    <field name="publisher">Collins</field>
  </doc>
  <doc>
  ...
  </doc>
</add>
```

`<commit/>` command to commit changes and make them searchable.

`<delete>` command can delete by UniqueID (if specified) or by query.

```xml
<delete>
  <id>0002166313</id>
  <id>0031745983</id>
  <query>subject:sport</query>
  <query>publisher:penguin</query>
</delete>
```

`<rollback/>` to return to last commit

Several commands can be grouped.

Example `curl` request:

```bash
curl http://localhost:8983/solr/my_collection/update -H "Content-Type: text/xml" --data-binary '
<add>
  <doc>
    <field name="authors">Patrick Eagar</field>
    <field name="subject">Sports</field>
    <field name="dd">796.35</field>
    <field name="isbn">0002166313</field>
    <field name="yearpub">1982</field>
    <field name="publisher">Collins</field>
  </doc>
</add>'
```

Or by passing a file:

```bash
curl http://localhost:8983/solr/my_collection/update -H "Content-Type: text/xml" -T "myfile.xml" -X POST
```

### JSON updates

#### Adding single JSON document

```bash
curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/my_collection/update/json/docs' --data-binary '
{
  "id": "1",
  "title": "Doc 1"
}'
```

#### Adding multiple JSON documents

```bash
curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/my_collection/update' --data-binary '
[
  {
    "id": "1",
    "title": "Doc 1"
  },
  {
    "id": "2",
    "title": "Doc 2"
  }
]'
```

#### Sending JSON update commands (similar to XML)

```bash
curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/my_collection/update' --data-binary '
{
  "add": {
    "doc": {
      "id": "DOC1",
      "my_field": 2.3,
      "my_multivalued_field": [ "aaa", "bbb" ]   # Can use array for multi-valued field
    }
  },
  "add": {
    "commitWithin": 5000, # Commit within 5 seconds
    "overwrite": false,  # Don't check for docs with same uniqueID
    "doc": {
      "f1": "v1", 
      "f1": "v2" # Can use repeated keys for multivalued fields
    }
  },

  "commit": {},
  "optimize": { "waitSearcher":false },

  "delete": { "id":"ID" },  
  "delete": { "query":"QUERY" } 
}'
```

#### Transforming Custom JSON

Refer to Solr documentation

### Delete all data

```bash
curl -X POST -H 'Content-Type: application/json' --data-binary '{"delete":{"query":"*:*" }}' http://localhost:8983/solr/my_collection/update
```

### Indexing Nested Documents

Schema configuration: a `_root_` field is required:

```xml
<field name="_root_" type="string" indexed="true" stored="false" docValues="false" />
```

Solr auto-populates this with the `id` value of the parent document.

Also, you should define a `_nest_path_` field-type.

```xml
<fieldType name="_nest_path_" class="solr.NestPathField" />
<field name="_nest_path_" type="_nest_path_" />`
```

This is auto-populated for child documents but not parent documents. This allows Solr to properly reconstruct the relationship.

<hr/>

## Searching

**Request handlers**: Defines logic when Solr processes a request

**Query parser**: For search queries, request handlers call a query parser.

**Faceting**: Arrangement of queries according to categories (based on indexed terms).

**Response Writer**: Presentation of the response, e.g. in JSON or XML

### Query Parameters

**`defType`**

Selects the query parser. E.g. `defType=dismax`. Default is the Standard Query Parser.

**`sort`**

Sort based on:

* Document scores
* Functions
* Value of primitive field which has `docValues='true'` (or `multivalued='false'` and `indexed='true'`)
* `SortableTextField`
* Single-valued text field thata uses and analyzer that produces only a single term per document.

**`start`**

Offset into query result set. For pagination purpose.

**`row`**

Paginate by specifying number of results.

**`fq`**

Filter query results without influencing score.

**`fl`** 

Limit response to a list of fields.

### Standard Query Parser

Also known as `lucene` parser. Robust and intuitive syntax, but more vulnerable to errors than `DisMax`.

#### Parameters

**`q`**

Defines the query using standard query syntax.

**`q.op`**

Default operator for query expressions.

**`df`**

Default searchable field

### Search on multiple fields

Use the `OR` operator.



<hr/>

## Authentication

### Enable Basic Authentication

`bin/solr auth enable` does the following:

1. Uploads a `security.json` file to ZooKeeper

2. Adds following lines to `bin/solr.in.sh`:

   ```bash
   # The following lines added by ./solr for enabling BasicAuth
   SOLR_AUTH_TYPE="basic"
   SOLR_AUTHENTICATION_OPTS="-Dsolr.httpclient.config=/path/to/solr-8.9.0/server/solr/basicAuth.conf"
   ```

3. Creates `server/solr/basicAuth.conf` file to store credential info.

**Options:**

`-credentials`

Username and password in form `username:password`.

## Zookeeper Operations

```bash
bin/solr zk
```

### Download a configset

```bash
./zkcli.sh -zkhost <zookeeper URL> -cmd downconfig -confdir <local directory> -confname <config name>
```

### Upload configset

```bash
bin/solr zk upconfig
```

**Options:**

`-n <name>`

Upload and give it the specified name

`-d <configset dir>`

The directory should have a `conf` subdirectory that in turn contains a `solrconfig.xml` file.

`-z <zkHost>`

Zookeeper connection string. Unnecessary if ZK_HOST is defined in `solr.in.sh`.

<hr/>

## Backups

### SolrCloud

Endpoint: 

```
/admin/collections?action=BACKUP
```

**Params**

| Name         | Purpose                                               |
| ------------ | ----------------------------------------------------- |
| `collection` | Name of collection                                    |
| `name`       | Backup name - cannot repeat a name                    |
| `location`   | Location on shared drive to write to.                 |
| `async`      | ID to track this async action                         |
| `repository` | If none specified, local filesystem repo will be used |

### Standalone

Using replication API:

```
/replication?command=backup
```

To restore:

```
/replication?command=restore&name=backup_name
```

