.PHONY: registry
registry:
	docker run -it --rm -p 5000:5000 ghcr.io/oras-project/registry:latest

.PHONY: save
save:
	docker save --output image.tar ${IMG}

.PHONY: syft
syft:
	docker run --rm -it \
	--volume /var/run/docker.sock:/var/run/docker.sock \
	--volume ./image.tar:/image.tar \
	--volume ./sbom:/sbom \
	--name Grype anchore/syft:latest --from docker-archive /image.tar -o spdx-json=/sbom/sbom.json

.PHONY: grype
grype:
	docker run --rm -it \
	--volume /var/run/docker.sock:/var/run/docker.sock \
	--volume ./sbom:/sbom \
	--volume ./cve:/cve \
	--name Grype anchore/grype:latest sbom:/sbom/sbom.json -o table -o cyclonedx-json=/cve/cve.json

# syft frontend:0.0.1 -o spdx-json=sbom-back-0.0.5.json
# grype sbom:./sbom/sbom.json
# oras discover ghcr.io/mathieu-junia/backend/artifact:cve --format tree
# oras pull ghcr.io/mathieu-junia/backend/artifact:cve