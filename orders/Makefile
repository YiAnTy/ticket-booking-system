build-image:
	docker build -t nameko/nameko-orderservice:$(TAG) .;

docker-tag:
	docker tag nameko/nameko-orderService:$(FROM_TAG) \
	nameko/nameko-orderService:$(TAG)

push-image:
	docker push nameko/nameko-orderService:$(TAG)
