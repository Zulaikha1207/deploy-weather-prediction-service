## Deploying weather prediction model on IBM cloud Pak for Data

Tools used:
- GitHub - code versioning
- DVC - data, model and metrics versioning and workflow orchestration (dvc repro)
- Terraform - setup IBM infrastructure using IaaC
- IBM Watson ML- Deploying ML models
- IBM Watson Openscale - Monitor model performance

![My Image](project_structure.png)

## Steps

- Create infrastructure on IBM cloud

**`terraform init, terraform plan , terraform apply`**

- Configure and authenticate Cloud Object Storage (DVC)

```python
dvc remote modify --local remote-storage access_key_id "..."
dvc remote modify --local remote-storage secret_access_key "..."
```

- Run dvc pipeline (dvc repro)

```python
dvc repro
```

- Push all data, metrics to the cloud
- Create workspace/deployment space

```python
python Infrastructure/datapak_manage.py (options)
```

- Deploy model to the cloud deployment space

```python
python src/pipeline/model_deploy_pipeline.py reports/train_pipe.joblib . ./credentials.yaml
```

- Update model API
- Send data request to deployed model API