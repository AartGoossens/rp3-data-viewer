build:
	docker-compose -p rp3-data-viewer -f docker/docker-compose.yml build

serve:
	docker-compose -f docker/docker-compose.yml up

deploy_dev: export VERSION=0.1.0

deploy_dev: build
	gcloud config configurations activate gssns
	gcloud config set project gssns-generic-310412
	docker tag rp3-data-viewer:latest gcr.io/gssns-generic-310412/rp3-data-viewer:latest
	docker push gcr.io/gssns-generic-310412/rp3-data-viewer:latest
	docker tag rp3-data-viewer:latest gcr.io/gssns-generic-310412/rp3-data-viewer:${VERSION}
	docker push gcr.io/gssns-generic-310412/rp3-data-viewer:${VERSION}
	gcloud run deploy rp3-data-viewer --platform managed --allow-unauthenticated --image gcr.io/gssns-generic-310412/rp3-data-viewer:${VERSION}
