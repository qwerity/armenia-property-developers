#!/usr/bin/env bash
# Deploy dist/ to S3 and invalidate CloudFront.
#
#   S3_BUCKET=my-bucket CLOUDFRONT_DISTRIBUTION_ID=E123ABC ./deploy.sh
#
# Requires the AWS CLI with credentials that can write the bucket and create invalidations.
set -euo pipefail

: "${S3_BUCKET:?set S3_BUCKET to the target bucket name}"
DIST_DIR="${DIST_DIR:-dist}"

if [ ! -d "$DIST_DIR" ]; then
  echo "$DIST_DIR not found - run: GOOGLE_MAP_API_KEY=... python3 build.py" >&2
  exit 1
fi

# Nothing is fingerprinted, so assets get an hour while the pages, config and dataset get five
# minutes; each deploy also invalidates the edge caches.
aws s3 sync "$DIST_DIR" "s3://$S3_BUCKET" --delete \
  --exclude "*.html" --exclude "config.js" --exclude "version.json" --exclude "data/*" \
  --cache-control "public, max-age=3600"

aws s3 sync "$DIST_DIR" "s3://$S3_BUCKET" \
  --exclude "*" --include "*.html" --include "config.js" --include "version.json" --include "data/*" \
  --cache-control "public, max-age=300"

if [ -n "${CLOUDFRONT_DISTRIBUTION_ID:-}" ]; then
  aws cloudfront create-invalidation --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths "/*" >/dev/null
  echo "invalidated $CLOUDFRONT_DISTRIBUTION_ID"
fi

echo "deployed $DIST_DIR to s3://$S3_BUCKET"
