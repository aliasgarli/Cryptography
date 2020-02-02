
class CeaserCipher:
    cipher_dict={'A':":-D",'B':"X-(",'C':"O:-)",'D':"B-)",'E':":-$",'F':":-*",'G':";-)",'H':":-(",'I':"|-)",'J':":-|",'K':":-)",'L':":->",'M':":-O",'N':":-/",'O':":-!",'P':":-P",'Q':":'-(",'R':":-X",'S':":-[",'T':":-]",'U':">:-|",'V':">:-(",'W':">:-)",'X':":-?",'Y':">:-P",'Z':";-D"}
    reverse_dict={":-D":'A',"X-(":'B',"O:-)":'C',"B-)":'D',":-$":'E',":-*":'F',";-)":'G',":-(":'H',"|-)":'I',":-|":'J',":-)":'K',":->":'L',":-O":'M',":-/":'N',":-!":'O',":-P":'P',":'-(":'Q',":-X":'R',":-[":'S',":-]":'T',">:-|":'U',">:-(":'V',">:-)":'W',":-?":'X',">:-P":'Y',";-D":'Z'}
    
    def __init__(self,clear_text,key):
        self.clear_text = clear_text
        self.key = key
        #self.ceaser_dict = cipher_dict

    
    def encrypt_text(self):
        encrypted_text = ""
        for letter in self.clear_text:
            #print(type(self.cipher_dict[letter]))
            encrypted_text += self.cipher_dict[letter]
            encrypted_text +=" "
        return encrypted_text

    def decrypt_text(self,encryption_text):
        decrypted_text = ""
        smile=''
        for i in encryption_text:
            if(i!=' '):
                smile +=i
            else:
                decrypted_text += self.reverse_dict[smile]
                smile = ''
        return decrypted_text
    
    def encrypt_key(self):
        encrypted_key = ""
        for letter in self.key:
            encrypted_key += self.cipher_dict[letter]
            encrypted_key +=" "
        return encrypted_key
   
    def decrypt_key(self):
        decrypted_key = ""
        smile = ''
        for i in encrypted_key:
            if(i!=' '):
                smile +=i
            else:
                decrypted_key +=self.reverse_dict[smile]
                smile = ''
        return decrypted_key
    

class VigenereTable(CeaserCipher):
    
    def __init__(self,cipher_dict):
        self.cipher_dict= super().cipher_dict
        self.smile_list =self.create_smile_list()
        #self.table = list()
    
    def create_smile_list(self):
        smile_list=list()
        for l_ord in range(ord('A'),ord('Z')+1):
            smile_list.append(self.cipher_dict[chr(l_ord)])
        return smile_list
    #smile_list = self.create_smile_list()
    
    def create_table(self,smile_list):
        number_of_smiles=len(smile_list)
        table=[]
        for row in range(number_of_smiles):
            array = list()
            for col in range(number_of_smiles):
                #print(smile_list[(col+row)%(number_of_smiles-1)])
                array += [smile_list[((col+row)%(number_of_smiles))]]
            table += [array]
            del array
        f = open("table_info.txt","w")
        tab_len=len(table) 
        line_len=len(table[0])
        for k in range(tab_len):
            for i in range(line_len):
                f.write(table[k][i])
                f.write(" ")
            f.write("\n")
        f.close()

        return table



class VigenereCipher():

    def __init__(self,ceaser_encrypted_text,ceaser_encrypted_key,smile_list,vigenere_table):
        self.text = ceaser_encrypted_text
        self.key = ceaser_encrypted_key
        self.smile_list = smile_list
        self.vigenere_table = vigenere_table

    
    def encrypt_message(self):
        vigenere_encrypted = ""

        # obtain text message encrypted with smiles
        array_t =list()
        smile_t= ""
        for i in self.text:
            if(i!=' '):
                smile_t += i
            else:
                array_t.append(self.smile_list.index(smile_t))
                smile_t = ""
        # obtain key encryted with smiles
     
        array_k =list()
        smile_k = ""
        for j in self.key:
            if(j!=' '):
                smile_k +=j
            else:
                array_k.append(self.smile_list.index(smile_k))
                smile_k = ""
        cipher_index = list()
        len_k =len(array_k)

        k_num = -1
        for t_num in array_t:
            k_num = (k_num+1)%len_k
            cipher_index.append((array_k[k_num],t_num))

        for k in cipher_index:
            #k[0],k[1]
            vigenere_encrypted +=self.vigenere_table[k[0]][k[1]]
            vigenere_encrypted +=" "
        
        return vigenere_encrypted


    def decrypt_message(self,vigenere_encrypted_text,vigenere_table):
        vigenere_decrypted = ""
        
        array_k =list()
        smile_k = ""
        for j in self.key:
            if(j!=' '):
                smile_k +=j
            else:
                array_k.append(self.smile_list.index(smile_k))
                smile_k = ""

        #array_k = self.convert_to_smile(self.key)
        
        key_len = len(array_k)

        message_indexes = list()
        smile_t = ""
        for k in vigenere_encrypted_text:
            if(k!=" "):
                smile_t += k
            else:
                message_indexes.append(self.smile_list.index(smile_t))
                smile_t = ""

        decrypted_index_list= list()

        # array_k
        key_in = -1
        for msi in message_indexes:
            key_in =(key_in + 1 )% key_len
            
            decrypted_index_list.append(vigenere_table[array_k[key_in]].index(self.smile_list[msi]))
        
        for i in decrypted_index_list:
            vigenere_decrypted += smile_list[i]
            vigenere_decrypted += " "

        return vigenere_decrypted
        


# DRIVER CODE

text=input("Enter text: ")
key = input("Enter key: ")

new_text=text.upper()
new_key=key.upper()


encryption = CeaserCipher(new_text,new_key)
encrypted_text = encryption.encrypt_text()
encrypted_key = encryption.encrypt_key()


print(f"Ceaser Encrypted text :\n{encrypted_text}")



Vigenere=VigenereTable(CeaserCipher)
smile_list=Vigenere.create_smile_list()
table=Vigenere.create_table(smile_list)




cipher=VigenereCipher(encrypted_text,encrypted_key,smile_list,table)
encrypted_message = cipher.encrypt_message()


print("cipher.encrypted_text:",cipher.text)
print("cipher.encrypted_key :",cipher.key)

print(f"Double encrypted message :\n{encrypted_message}")
decrypted_cipher_text = cipher.decrypt_message(encrypted_message,table)

print(f"Vigenere Decrypted Text:\n{decrypted_cipher_text}")

final_decrypted_message =encryption.decrypt_text(decrypted_cipher_text)
print(f"Final decrypted message:\n{final_decrypted_message}")
