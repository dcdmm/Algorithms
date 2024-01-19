#include <string>
#include <vector>
#include <iostream>

using namespace std;

/**
 * 字典树的(Array Trie)实现
 */
class Trie {
private:
    vector<Trie *> children;
    bool isEnd; // 是否为字符串结尾

    /**
     * @brief 查找前缀
     */
    Trie *searchPrefix(string prefix) {
        Trie *node = this;
        for (char ch: prefix) {
            ch -= 'a';
            if (node->children[ch] == nullptr) {
                return nullptr;
            }
            node = node->children[ch];
        }
        return node;
    }

public:
    Trie() : children(26), isEnd(false) {} // Trie *默认值为:nullpter

    /**
     * @brief 插入字符串
     */
    void insert(string word) {
        Trie *node = this; // this指针
        for (char ch: word) {
            ch -= 'a';
            // "->"运算符:访问指针所指向对象的成员变量或成员函数
            if (node->children[ch] == nullptr) {
                node->children[ch] = new Trie();
            }
            node = node->children[ch];
        }
        node->isEnd = true;
    }

    bool search(string word) {
        Trie *node = this->searchPrefix(word);
        return node != nullptr && node->isEnd;
    }

    bool startsWith(string prefix) {
        return this->searchPrefix(prefix) != nullptr;
    }
};

int main() {
    Trie t = Trie();
    t.insert("apple");
    cout << t.search("apple") << endl;
    cout << t.search("app") << endl;
    cout << t.startsWith("app") << endl;
    t.insert("app");
    cout << t.search("app") << endl;
}