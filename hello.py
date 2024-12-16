from rich.progress import Progress
import sys
import requests

if len(sys.argv) != 2:
    print("Usage: python hello.py <manifest_url>")
    sys.exit(1)

manifest_url = sys.argv[1]


# example download url: https://digi.vatlib.it/pub/digit/MSS_Ross.424/iiif/Ross.424_0013_fa_0004r.jp2/full/898,/0/native.jpg
# example id: https://digi.vatlib.it/iiifimage/MSS_Ross.424/Ross.424_0006_cy_0002v.jp2
def main():
    manifest = requests.get(manifest_url).json()
    images = [
        image
        for sequence in manifest["sequences"]
        for canvas in sequence["canvases"]
        for image in canvas["images"]
    ]

    with Progress() as progress:
        task = progress.add_task("Downloading...", total=len(images))

        for image in images:
            width = int(image["resource"]["width"])
            id = image["resource"]["service"]["@id"]
            url = id.replace("iiifimage", "pub/digit")
            url_parts = url.split("/")
            url = "/".join(url_parts[:-1]) + "/iiif" + "/" + url_parts[-1]
            url += f"/full/{width},/0/native.jpg"
            img = requests.get(url)
            filename = f"{image['resource']['service']['@id'].split('/')[-1]}.jpg"  # Assuming the label is not available, using the image ID instead
            progress.update(task, description=f"Downloading {filename}")
            with open(filename, "wb") as f:
                f.write(img.content)
            progress.advance(task)


if __name__ == "__main__":
    main()
