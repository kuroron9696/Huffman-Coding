# coding: utf-8
import re
import collections

def output_conditions():
    print("<<入力する文字列は次の条件を満たしてください。>>")
    print("1.使用する文字が小文字のアルファベットのみ")
    print("2.文字列の長さが40文字以下")
    print("3.文字の種類が10種類以下\n")

# 生起確率を計算するメソッド
def compute_occurrence_probability(number_of_chars,collections_array):
  occurrence_probability_array = [ [collections_array[i][0],collections_array[i][1]/number_of_chars] for i in range(len(collections_array))]
  return occurrence_probability_array

# ハフマン木の葉を示すクラス
class Node:
  # コンストラクタ
  def __init__(self,char = None,occurrence_probability = None,left = None,right = None):
    self.char = char
    self.occurrence_probability = occurrence_probability
    self.left = left
    self.right = right

# ハフマン木を示すクラス
class HuffmanTree:
  # コンストラクタ
  def __init__(self,input_string,string_array,string_collections,collections_array,occurrence_probability_array):
    self.encode_dict = {}
    self.input_string = input_string
    self.string_array = string_array
    self.string_collections = string_collections
    self.collections_array = collections_array
    self.occurrence_probability_array = occurrence_probability_array

  # 符号化するメソッド
  def encode(self):
    nodes = [] # 探索していない葉を格納する配列

    # 葉の生成
    for i in range(len(self.collections_array)):
      nodes.append(Node(self.occurrence_probability_array[i][0],self.occurrence_probability_array[i][1]))

    temp = []

    # 探索していない葉が1つになるまで繰り返す
    while len(nodes) > 1:
      # 生起確率の最も小さい2つの葉の生起確率を合計して新しい葉を生成
      for i in range(2):
        element = nodes[-1]
        temp.append(element)
        nodes.remove(element)

      # 新しい葉を生成
      new_node = Node(char=None, occurrence_probability=temp[0].occurrence_probability+temp[1].occurrence_probability, right=temp[0], left=temp[1])
      temp = []
      # 探索していない葉の配列に格納
      nodes.append(new_node)

    # 符号語の割り当て
    self.allocate_codewords(nodes[0],"")
    return self.encode_dict

  # 符号語を割り当てるメソッド
  # 再帰構造
  def allocate_codewords(self,node,code):

    # nodeがクラスNodeのオブジェクトでないときreturn
    if not isinstance(node, Node):
      return

    # 葉が文字を持っている(節点でない)場合、符号語を割り当ててreturn
    if node.char:
      self.encode_dict[node.char] = code
      return

    # 再帰呼び出し
    self.allocate_codewords(node.left, code+"0")
    self.allocate_codewords(node.right, code+"1")

if __name__ == "__main__":
  print("[ハフマン符号の構成プログラム]\n")
  output_conditions()
  input_string = input("符号化したい文字列を入力\n>>")
  print("\n")
  pattern = re.compile("[a-z]+") # 小文字のアルファベットの正規表現パターンを作成
  string_array = list(input_string) # 入力文字列を配列に変換
  error_strings = [] # 制限を越えた文字列の配列
  string_collections = collections.Counter(string_array) # 文字の種類と出現回数を保持するオブジェクト
  collections_array = string_collections.most_common() # 文字の種類と出現回数を配列に変換

  # 入力文字列がパターンにマッチしない
  # 入力文字列の長さが40文字より大きい
  # 文字の種類が10より大きい
  # 上記のいずれかの条件を満たしたら再入力
  while((not pattern.fullmatch(input_string)) or len(input_string) > 40 or len(string_collections) > 10):
    error_strings.append(input_string)
    output_conditions()
    input_string = input("再入力\n>>")
    print("\n")
    string_array = list(input_string)
    string_collections = collections.Counter(string_array)
    collections_array = string_collections.most_common()

  occurrence_probability_array = compute_occurrence_probability(len(input_string),collections_array) # 生起確率と文字の組となる2次元配列を作成
  Huffman_Tree = HuffmanTree(input_string,string_array,string_collections,collections_array,occurrence_probability_array) # ハフマン木をインスタンス生成
  codewords = Huffman_Tree.encode() # 入力文字列を符号化
  codewords_array = list(codewords.items()) # 文字と符号語の組の辞書型を配列に変換
  result = [ [collections_array[i][0],collections_array[i][1],occurrence_probability_array[i][1],codewords_array[i][1]] for i in range(len(collections_array))] # 結果をまとめる

  print("\n[入力した文字列]")
  print(input_string+"\n")
  print("文字","文字数","出現確率","ハフマン符号")
  # 結果の出力
  for output in result:
    print("|",output[0],"|",output[1],"|",output[2],"|",output[3])
