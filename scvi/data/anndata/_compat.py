from anndata import AnnData

from . import _constants
from ._fields import CategoricalObsField, LayerField
from ._manager import AnnDataManager


def manager_from_setup_dict(
    adata: AnnData, setup_dict: dict, **transfer_kwargs
) -> AnnDataManager:
    source_adata_manager = AnnDataManager()
    data_registry = setup_dict[_constants._DATA_REGISTRY_KEY]
    for scvi_key, adata_mapping in data_registry.items():
        field = None
        attr_name = adata_mapping[_constants._DR_ATTR_NAME]
        attr_key = adata_mapping[_constants._DR_ATTR_KEY]
        if attr_name == _constants._ADATA_ATTRS.X:
            field = LayerField(scvi_key, None)
        elif attr_name == _constants._ADATA_ATTRS.LAYERS:
            field = LayerField(scvi_key, attr_key)
        elif attr_name == _constants._ADATA_ATTRS.OBS:
            field = CategoricalObsField(scvi_key, attr_key)
        else:
            raise NotImplementedError(
                f"Backwards compatibility for attribute {attr_name} is not implemented yet."
            )
        source_adata_manager.add_field(field)
    return source_adata_manager.transfer_setup(
        adata, setup_dict=setup_dict, **transfer_kwargs
    )
