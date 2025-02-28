Below is an example of how you can **build your own Docker image locally** (instead of using the `evenchange4/docker-tfjs-converter` image) and then run **`tensorflowjs_converter`** with that local image.

---

## 1. Create a Dockerfile

Create a file named **`Dockerfile`** (no extension) in your project directory with the contents:

```dockerfile
# Example: Use Python 3.10 (or a compatible version) as the base
FROM python:3.10

# Install any required packages
#  - tensorflowjs includes the converter
#  - you can also install tensorflow if you need local conversions
RUN pip install --no-cache-dir tensorflowjs

# Set a working directory in the container
WORKDIR /converter

# By default, run the "tensorflowjs_converter" entrypoint
ENTRYPOINT ["tensorflowjs_converter"]
```

### **Explanation:**

- **FROM python:3.10** → Uses Python 3.10 (you can pick a different Python version if needed).
- **RUN pip install tensorflowjs** → Installs the TensorFlow.js converter script.
- **WORKDIR /converter** → Default working directory.
- **ENTRYPOINT** → Makes it so that any extra parameters you pass to `docker run` after the image name are interpreted as arguments to `tensorflowjs_converter`.

---

## 2. Build Your Local Docker Image

In the same folder as the **`Dockerfile`**, run:

```bash
docker build -t local-tfjs-converter .
```

This will create a Docker image named **`local-tfjs-converter`**.

---

## 3. Run the Container

Use the same volume mounts and arguments as your original command, but replace the image name (`evenchange4/docker-tfjs-converter`) with **`local-tfjs-converter`**.

For example, if your original command was:

```bash
docker run -it --rm \
  -v "$PWD/python:/python" \
  evenchange4/docker-tfjs-converter \
  tensorflowjs_converter --input_format=keras python/output/model.h5 python/output/model-tfjs
```

Now you can do:

```bash
docker run -it --rm \
  -v "$PWD/python:/converter/python" \
  local-tfjs-converter \
  --input_format=keras \
  python/output/model.h5 \
  python/output/model-tfjs
```

### **Notes:**

1. **`-v "$PWD/python:/converter/python"`** → You’re mounting your local `python/` folder into `/converter/python` (since our `WORKDIR` is `/converter`).
2. You don’t need to explicitly write `tensorflowjs_converter` inside the container command because our **ENTRYPOINT** is already set to `["tensorflowjs_converter"]`. Instead, you directly pass the converter arguments.
3. Make sure the **paths** match correctly. In the container, you’ll see your model file at `python/output/model.h5` (under `/converter/python/output/model.h5`).

---

## 4. Verify the Conversion

When complete, the output (`model.json` + weight shards) will be written to `python/output/model-tfjs` inside the container. Thanks to the `-v` volume mount, you’ll see these files in your **local** `python/output/model-tfjs` folder.

---

## **Summary**

1. **Create a Dockerfile** with `FROM python:3.10` and `RUN pip install tensorflowjs`.  
2. **Build** the image:  

   ```bash
   docker build -t local-tfjs-converter .
   ```  

3. **Run** your conversion command, mounting your local directory:  

   ```bash
   docker run --rm -it \
     -v "$PWD/python:/converter/python" \
     local-tfjs-converter \
     --input_format=keras \
     python/output/model.h5 \
     python/output/model-tfjs
   ```  

4. **Check** the newly created `model.json` & shards in `python/output/model-tfjs`.

This replicates the original `evenchange4/docker-tfjs-converter` usage with your own local Dockerfile!

```
docker run --rm -v $(pwd):/workspace tfjs_converter --input_format=keras model.h5 web_model
```