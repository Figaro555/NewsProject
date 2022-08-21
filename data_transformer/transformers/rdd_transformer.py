class RDDTransformer:

    def find_words(self, data: dict, words: dict):
        try:
            data["word_in_text"] = sum([data["text"].lower().count(i) for i in words[data["country"]]])
            data["word_in_text_found"] = 1 if data["word_in_text"] > 0 else 0

            data["word_in_title"] = sum([data["title"].lower().count(i) for i in words[data["country"]]])
            data["word_in_title_found"] = 1 if data["word_in_title"] > 0 else 0
            return data
        except Exception as _ex:
            raise Exception("Schema or config file is incorrect")
