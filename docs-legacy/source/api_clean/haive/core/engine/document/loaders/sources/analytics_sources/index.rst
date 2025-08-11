
haive.core.engine.document.loaders.sources.analytics_sources
============================================================

.. py:module:: haive.core.engine.document.loaders.sources.analytics_sources

.. autoapi-nested-parse::

   Data processing and analytics platform source registrations.

   This module implements data processing, analytics, and ETL platform loaders including:
   - Data processing frameworks (Spark, Databricks, Snowflake)
   - Analytics platforms (Tableau, Power BI, Looker)
   - ETL/ELT tools (Fivetran, Stitch, Apache Airflow)
   - Time series databases (InfluxDB, TimescaleDB, Prometheus)
   - Log analytics (Elasticsearch, Splunk, Datadog)






Functions
---------

   get_analytics_sources_statistics   validate_analytics_sources   detect_analytics_platform
.. autofunction:: get_analytics_sources_statistics
.. autofunction:: validate_analytics_sources
.. autofunction:: detect_analytics_platform

Classes
-------

* :py:class:`AnalyticsPlatform` - Analytics and data processing platforms.* :py:class:`QueryType` - Types of analytical queries.* :py:class:`DataFormat` - Data export formats.* :py:class:`SnowflakeSource` - Snowflake data warehouse source.* :py:class:`DatabricksSource` - Databricks SQL warehouse source.* :py:class:`BigQuerySource` - Google BigQuery data warehouse source.* :py:class:`TableauSource` - Tableau analytics platform source.* :py:class:`PowerBISource` - Microsoft Power BI source.* :py:class:`InfluxDBSource` - InfluxDB time series source.* :py:class:`PrometheusSource` - Prometheus metrics source.* :py:class:`ElasticsearchSource` - Elasticsearch log analytics source.* :py:class:`SplunkSource` - Splunk log analytics source.* :py:class:`KafkaSource` - Apache Kafka streaming source.* :py:class:`AirflowSource` - Apache Airflow ETL platform source.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/AnalyticsPlatform   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/QueryType   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/DataFormat   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/SnowflakeSource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/DatabricksSource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/BigQuerySource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/TableauSource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/PowerBISource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/InfluxDBSource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/PrometheusSource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/ElasticsearchSource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/SplunkSource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/KafkaSource   /api_clean/haive/core/engine/document/loaders/sources/analytics_sources/AirflowSource

Package Contents
----------------

