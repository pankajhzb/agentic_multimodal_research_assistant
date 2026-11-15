
# Document Generation and Scheduled Calculations

The document service generates claim acknowledgement letters, assessment summaries and decision letters from approved templates. Generated documents are associated with the claim identifier and stored with metadata including document type, version, creation time and creator.

Scheduled calculation jobs process eligible claims in controlled batches. Jobs must be restartable and idempotent. Each run records its start time, end time, status, processed record count and failure details. Failed records should be isolated for retry or manual investigation rather than causing duplicate business transactions.
