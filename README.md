# tiyaro-cli-examples
Sample model projects to demonstrate / test model onboarding to Tiyaro Infra using [Tiyaro CLI](https://pypi.org/project/tiyaro/)

### Installation
```
pip install tiyaro
```

# PyTorch
Sample PyTorch models onboarded to Tiyaro Infra

## ALEXNET
[Model Source](https://github.com/Lornatang/AlexNet-PyTorch)

[Handler](./AlexNet/tiyaro_handler/) shows a simple Image Classification example. Check project's [README](./AlexNet/README.md) for more details about the project.

- [x] [Tiyaro Model Card](https://console.tiyaro.ai/explore/trn:model:123456789012-venkat:1.0:alexnetpy_dc50d8)
- [x] API available
- [x] Verified using Tiyaro CLI Version `0.0.6`

## SWINIR
[Model Source](https://github.com/JingyunLiang/SwinIR)

[Handler](./SwinIR/tiyaro_handler/) shows only one example for Image Restoration.  There are 10+ pre-trained files and models in this repo.  Check project's [README](./SwinIR/README.md) and [Test](./SwinIR/main_test_swinir.py) for writing handlers for other models.

- [x] [Tiyaro Model Card](https://console.tiyaro.ai/explore/trn:model:123456789012-venkat:1.0:swinir_classicalsr_div2k_scale2_status2_899ec8)
- [x] API available
- [x] Verified using Tiyaro CLI Version `0.0.6`

## GFPGAN
[Model Source](https://github.com/TencentARC/GFPGAN)

[Handler](./GFPGAN/tiyaro_handler/) shows only one example model for Image Enhancement.  Check project's [README](./GFPGAN/README.md) for writing handlers for other models.

- [x] [Tiyaro Model Card](https://console.tiyaro.ai/explore/trn:model:123456789012-smainkar:1.0:GFPGAN_680907)
- [x] API available
- [x] Verified using Tiyaro CLI Version `0.0.4.dev9`

## PSPNet
[Model Source](https://github.com/yassouali/pytorch-segmentation)

[Handler](./PSPNet/tiyaro_handler/) shows only one example model for Image Segmentation. Check project's [README](./PSPNet/README.md)  for writing handlers for other models.

- [x] [Tiyaro Model Card](https://console.tiyaro.ai/explore/trn:model:123456789012-smainkar:1.0:PSPNet_ef885d)
- [x] API available
- [x] Verified using Tiyaro CLI Version `0.0.4.dev9`


## MAGMA
[Model Source](https://github.com/Aleph-Alpha/magma)

[Handler](./magma/tiyaro_handler/) shows example tiyaro handler based on this model's [README](./magma/README.md) and [Example](./magma/example_inference.py). The pre-trained file for this model is 12.1GB and it has exposed stress points in Tiyaro Push MVP setup.  WIP.