==============================
Transfer learning
==============================

In scvi-tools, transfer learning is currently supported for the subset of models that represent the data
in a lower-dimensional space (e.g., scVI, totalVI). For these particular models, which belong to a class of
models called conditional variational autoencoders (cVAEs), transfer learning
is tantamount to ingesting new data in order to analyze it in the context of some reference dataset.
For this, we use the scArches approach [#ref1]_.



Reference mapping with scArches
===============================

The core logic for scArches is implemented in :class:`~scvi.model.base.ArchesMixin`.

.. topic:: Tutorials:

 - :doc:`/tutorials/notebooks/scarches_scvi_tools`

Preliminaries
-------------

scArches is an approach that works with cVAEs. Suppose we have :math:`G`-dimensional gene expression data represented by :math:`x` and one categorical covariate with :math:`K`
categories that is represented via one-hot (i.e., the second category would be represented as :math:`[0, 1, 0, ..., 0]`).
The first layer of the encoder with :math:`H` hidden neurons of a cVAE with ReLU activation can be written as

.. math::
   :nowrap:

   \begin{align}
   f_1(x,s) = {\textrm{max}}(0,W_x^{(1)} x + W_s^{(1)} s),
   \end{align}

where :math:`W_x^{(1)} \in \mathbb{R}^{H \times G}` and :math:`W_s^{(1)} \in \mathbb{R}^{H \times K}`.

Architectural surgery
---------------------

Now suppose our cVAE has been trained on data. The so-called "architectural surgery" with scArches augments the first layer with new parameters corresponding
to :math:`L` unseen categories in the query data (i.e., batches in single-cell language), which are represented in the one-hot vector :math:`s'`.

The first layer of the encoder is now specified as

.. math::
   :nowrap:

   \begin{align}
   f_1(x,s,s') = {\textrm{max}}(0,W_x^{(1)} x + W_s^{(1)} s + W_{s'}^{(1)} s'),
   \end{align}

where :math:`W_{s'} \in \mathbb{R}^{H \times L}` is a new randomly initialized matrix.
We note that in practice, there is only one matrix and not three separate matrices.
Also, with scArches, the same architectural surgery is applied to the decoder, which is not shown here for brevity.

Some of the cVAEs in scvi-tools use the categorical one-hot encodings in all hidden layers in the encoder.
For example, the option ``deeply_inject_covariates=True`` can be used in :class:`~scvi.model.SCVI`.
Empirically, this improves removal of nuisance variation due to these covariates.
In this case of "deep injection" there would be new parameters in each hidden layer. With two hidden layers
this is written as

.. math::
   :nowrap:

   \begin{align}
   f_2(x,s, s') = {\textrm{max}}(0,f_1(x,s, s') + W^{(2)}_s s + W^{(2)}_{s'} s').
   \end{align}


Training
--------

By default, the training of the model with the query data is performed with respect to only the new query-category specific parameters.
Thus, all the previous parameters from the reference building stage are frozen.
This results in a model in which the latent representation :math:`z` (encoder output) does not change for reference data after the
query step.


.. topic:: References:

   .. [#ref1] Mohammad Lotfollahi, Mohsen Naghipourfar, Malte D. Luecken, Matin Khajavi, Maren Büttner, Marco Wagenstetter, Ziga Avsec, Adam Gayoso, Nir Yosef, Marta Interlandi, Sergei Rybakov, Alexander V. Misharin, and Fabian J. Theis (2021),
        *Mapping single-cell data to reference atlases by transfer learning.*,
        `Nature Biotechnology <https://www.nature.com/articles/s41587-021-01001-7>`__.
