# AWS SS3

## Find largest file in bucket

```bash
aws s3api list-objects-v2 --bucket bucket-name --query "sort_by(Contents, &Size)[-1:]"
```

