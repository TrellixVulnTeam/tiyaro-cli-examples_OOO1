# tiyaro-push-examples
Sample model projects to demonstrate / test model onboarding to Tiyaro Infra

# PyTorch

## SWINIR
[Model Source](https://github.com/JingyunLiang/SwinIR)

[Handler](./SwinIR/tiyaro_handler/) shows only one example model.  There are 10+ pre-trained files and models in this repo.  Check project's [README](./SwinIR/README.md) and [Test](./SwinIR/main_test_swinir.py) for writing handlers for other models.

- [x] Generated MAR file using Tiyaro push infra
- [x] API available to do inference

## MAGMA
[Model Source](https://github.com/Aleph-Alpha/magma)

[Handler](./magma/tiyaro_handler/) shows example tiyaro handler based on this model's [README](./magma/README.md) and [Example](./magma/example_inference.py). The pre-trained file for this model is 12.1GB and it has exposed stress points in Tiyaro Push MVP setup.  WIP.

- [] Generated MAR file using Tiyaro push infra
- [] API available to do inference