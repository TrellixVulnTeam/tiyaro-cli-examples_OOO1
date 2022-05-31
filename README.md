# Tiyaro CLI
[Tiyaro CLI](https://pypi.org/project/tiyaro/) allows you to convert your github repo into a fully functional API. Complete with its own dedicated model card, sample code snippets, and swagger spec for your users, 
colleagues to discover your model and easily incorporate it into their smart applications.

### Installation
```
pip install tiyaro
```

# Tiyaro CLI Examples
Sample model projects to demonstrate / test model onboarding to Tiyaro Infra using Tiyaro CLI

## PyTorch
Sample PyTorch models onboarded to Tiyaro Infra

### ALEXNET

<a href="https://console.tiyaro.ai/explore/trn:model:123456789012-venkat:1.0:alexnetpy_dc50d8">
<img src="https://tiyaro-public-docs.s3.us-west-2.amazonaws.com/assets/tiyaro-badge.svg"></a>


[Model Source](https://github.com/Lornatang/AlexNet-PyTorch)

[Handler](./AlexNet/tiyaro_handler/) shows a simple `Image Classification` example. Check project's [README](./AlexNet/README.md) for more details about the project.

- [x] [Tiyaro Model Card](https://console.tiyaro.ai/explore/trn:model:123456789012-venkat:1.0:alexnetpy_dc50d8)
- [x] API available
- [x] Verified using Tiyaro CLI Version `0.0.8`

### FLAIR-TEXT-CLASSIFICATION

<a href="https://console.tiyaro.ai/explore/trn:model:123456789012-venkat:1.0:FLAIR_TEXT_CLASSIFICATION_0e19a4">
<img src="https://tiyaro-public-docs.s3.us-west-2.amazonaws.com/assets/tiyaro-badge.svg"></a>


[Model Source](https://github.com/JingyunLiang/SwinIR)

[Handler](./SwinIR/tiyaro_handler/) shows only one example for Image Restoration.  There are 10+ pre-trained files and models in this repo.  Check project's [README](./SwinIR/README.md) and [Test](./SwinIR/main_test_swinir.py) for writing handlers for other models.

- [x] [Tiyaro Model Card](https://console.tiyaro.ai/explore/trn:model:123456789012-venkat:1.0:SWINIR_899ec8)
- [x] API available
- [x] Verified using Tiyaro CLI Version `0.0.8`

### GFPGAN

<a href="https://console.tiyaro.ai/explore/trn:model:123456789012-smainkar:1.0:GFPGAN_680907">
<img src="https://tiyaro-public-docs.s3.us-west-2.amazonaws.com/assets/tiyaro-badge.svg"></a>


[Model Source](https://github.com/TencentARC/GFPGAN)

[Handler](./GFPGAN/tiyaro_handler/) shows only one example model for Image Enhancement.  Check project's [README](./GFPGAN/README.md) for writing handlers for other models.

- [x] [Tiyaro Model Card](https://console.tiyaro.ai/explore/trn:model:123456789012-smainkar:1.0:GFPGAN_680907)
- [x] API available
- [x] Verified using Tiyaro CLI Version `0.0.4.dev9`

### PSPNet

<a href="https://console.tiyaro.ai/explore/trn:model:123456789012-smainkar:1.0:PSPNet_ef885d">
<img src="https://tiyaro-public-docs.s3.us-west-2.amazonaws.com/assets/tiyaro-badge.svg"></a>


[Model Source](https://github.com/yassouali/pytorch-segmentation)

[Handler](./PSPNet/tiyaro_handler/) shows only one example model for Image Segmentation. Check project's [README](./PSPNet/README.md)  for writing handlers for other models.

- [x] [Tiyaro Model Card](https://console.tiyaro.ai/explore/trn:model:123456789012-smainkar:1.0:PSPNet_ef885d)
- [x] API available
- [x] Verified using Tiyaro CLI Version `0.0.4.dev9`


### MAGMA
[Model Source](https://github.com/Aleph-Alpha/magma)

[Handler](./magma/tiyaro_handler/) shows example tiyaro handler based on this model's [README](./magma/README.md) and [Example](./magma/example_inference.py). The pre-trained file for this model is 12.1GB and it has exposed stress points in Tiyaro Push MVP setup.  WIP.

# Model Types
We have curated the open source community, model hubs and popular AI vendors to make sure you have access to the best AI models. Each model in the Tiyaro universe has its own API URL.  Examples are `image-classification`, `image-object-detection`, `text-classification`, etc., The full list of model types is [here](https://github.com/tiyaro/code-samples/tree/main/python).  

Tiyaro CLI currently supports the `image-classification` and `text-classification` model types. New model types are being added as we speak. If a model type is currently not supported by the CLI please reachout to us
at help@tiyaro.ai with your request.

# Supported Frameworks
Currently, only `PyTorch` is supported. We are actively working on adding support to more frameworks. Reachout to us at help@tiyaro.ai with your request for any other framework.