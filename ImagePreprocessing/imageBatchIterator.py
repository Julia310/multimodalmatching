import logging


class ImageBatchIterator:
    """
        Creates batches from data of the given image_path_list for image data preprocessing
        and the following image embedding generation.
        image_path_list has the following form:
            [{'articleId': 'TO112O055-C11', 'path': 'image1.jpg', 'brand': 'tommy hilfiger', 'url': 'https://...', 'data_alias': 'zal'},
             {'articleId': 'TO182H01V-G11', 'path': 'image2.jpg', 'brand': 'tommy hilfiger', 'url': 'https://...', 'data_alias': 'zal'},
             ...]
    """

    def __init__(self, image_path_list):
        self.image_path_list = image_path_list
        self.batch_size = 1000
        self.idx = 0

    def next_batch(self):
        if self.idx == len(self.image_path_list):
            return None

        idx_max = len(self.image_path_list)
        if self.idx + self.batch_size < idx_max:
            idx_max = self.idx + self.batch_size

        image_path_sublist = self.image_path_list[self.idx:idx_max]

        logging.info('>>>>>>>>>>  Preprocessing images    ' + str(self.idx) + ' - ' + str(idx_max) + '  <<<<<<<<<<')
        self.idx = idx_max
        return image_path_sublist
