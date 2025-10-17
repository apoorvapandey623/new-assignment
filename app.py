flask-k8s/
├── app.py
├── requirements.txt
├── Dockerfile
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
└── k8s/
    ├── namespace.yaml
    ├── deployment.yaml
    ├── service.yaml
    ├── hpa.yaml
    ├── ingress.yaml        # optional
    └── prometheus-rules.yaml
