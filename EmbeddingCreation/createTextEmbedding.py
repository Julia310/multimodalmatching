from transformers import AutoTokenizer, AutoModel
import torch
import pickle
from tqdm import tqdm
from dataAlias import ZALANDO_TABLE_ALIAS


def mean_pooling(model_output, attention_mask):
    """
        Mean Pooling - Take attention mask into account for correct averaging
    """
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


class TransformersEmbeddingGenerator:
    """
        Generates text embeddings by utilizing the given sentence transformer model.
    """
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model_name = AutoModel.from_pretrained(model_name)

    def create_text_embeddings(self, text):
        encoded_input = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')

        with torch.no_grad():
            model_output = self.model_name(**encoded_input)

        sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
        return sentence_embeddings.cpu().detach().numpy()


class ManageTextEmbeddings:
    """
        Receives the preprocessed Zalando text data within the text_df_zal dataframe and the preprocessed
        Tommy Hilfiger / Gerry Weber Text data in the text_df_th_gw.
        Obtains the text embeddings from the TransformersEmbeddingGenerator and saves the embeddings as well as the
        price float value in the database for later threshold_classification
    """

    def __init__(self, model_name, text_df_zal, text_df_th_gw, data_alias_zal, data_alias_th_gw, db_embedding_manager):
        self.model_name = model_name
        self.text_df_zal = text_df_zal
        self.text_df_th_gw = text_df_th_gw
        self.embedding_generator = TransformersEmbeddingGenerator(model_name=model_name)
        self.data_alias_zal = data_alias_zal
        self.data_alias_th_gw = data_alias_th_gw
        self.db_manager = db_embedding_manager

    def manage_embeddings(self):
        attributes = list(self.text_df_zal.columns)
        text_df_list = [(self.text_df_zal, self.data_alias_zal), (self.text_df_th_gw, self.data_alias_th_gw)]
        for j in range(len(text_df_list)):
            (text_df, data_alias) = text_df_list[j]
            emb_list = []
            indices = list(text_df.index)
            with tqdm(total=len(indices), desc='generate embeddings for dataset ' + str(j + 1), position=0, leave=True) as pbar:
                for i in range(len(indices)):
                    pbar.update()
                    embeddings = self.create_embeddings_for_row(indices[i], attributes, text_df.loc[[indices[i]]])
                    emb_list.append(embeddings)
            self.save_embeddings(emb_list, data_alias)

    def create_embeddings_for_row(self, index, columns, row):
        values = {'articleId': index}
        for col in columns:
            if not col == 'price':
                vector = self.embedding_generator.create_text_embeddings(row[col][0])[0]
                embed_bytes = pickle.dumps(vector)
                values[col] = embed_bytes
            else:
                values[col] = row[col][0]
        values['image'] = b'default'
        return values

    def save_embeddings(self, emb_ist, data_alias):
        if data_alias == ZALANDO_TABLE_ALIAS:
            self.db_manager.save_zalando_embeddings(emb_ist)
        else:
            self.db_manager.save_th_gw_embeddings(emb_ist)





