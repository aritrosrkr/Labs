def postorder(preorder, inorder):
    if not preorder or not inorder:
        return []

    root = preorder[0]
    root_index = inorder.index(root)

    left_inorder = inorder[:root_index]
    right_inorder = inorder[root_index+1:]

    left_preorder = preorder[1:1+len(left_inorder):]
    right_preorder = preorder[1+len(left_inorder)::]

    left_postorder = postorder(left_preorder, left_inorder)
    right_postorder = postorder(right_preorder, right_inorder)

    return left_postorder + right_postorder + [root]