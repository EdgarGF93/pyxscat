import pytest
from pygix.transform import Transform
from edf import EdfClass

class TestEdfClass(Transform):

    def __init__(
        self,
        filename=str(),
        dict_setup=dict(),
        name_setup=str(),
        json_file_setup=str(),
        transform_q=None,
        ponifile_path=str(),
        qz_parallel=True,
        qr_parallel=True,
    ):
        self.edf = EdfClass(
            filename=filename,
            dict_setup=dict_setup,
            name_setup=name_setup,
            json_file_setup=json_file_setup,
            transform_q=transform_q,
            ponifile_path=ponifile_path,
            qz_parallel=qz_parallel,
            qr_parallel=qr_parallel,
        )

    def test_qz_parallel(self):
        self.edf.set_qz_parallel(
            qz_parallel=True,
        )
        assert self.edf._qz_parallel == True

        self.edf.set_qz_parallel(
            qz_parallel=False,
        )
        assert self.edf._qz_parallel == False
