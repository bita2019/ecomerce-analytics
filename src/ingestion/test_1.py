# # carpet , carear => car , common prefix , a[n] == a[1]
# # carear 

# def find_prefix(a):
#     common_prefix = a[0] 
#     # result =[]
#     for i in range(len(common_prefix)):
#         cha = a[0][i]
#         print ('char =', cha)
#         for word in a[1:]:
#             print('word',word)
#             if i >= len(word) or word[i] != cha :
#                 return a[0][:i]
#     return a[0]
            
            
            
# b = find_prefix(['carear','carpet','ca'])
# print (b)
    
    # [carpet,carear] ==> car 
    # c,c  a,a  r,r ....  
    # c
# def lo(a):
#     # if Not a:
#     #     return None
#     for i in range(len(a)):
#         char = a[0][i] 
#         for word in a[1:]:
#             if i >= len(word) or word[i] != char:
#                 return a[0][:i]
#     return a[0]

# n = lo(['carear','carpet','car'])
# print (n)
        
def lo(a):
    for i in range(len(a[0])):
        char = a[0][i]
        for word in a[1:]:
            if i >= len(word) or word[i] != char:
                return a[0][:i]
    return a[0]

n = lo(['carear','carpet','car'])
print(n)