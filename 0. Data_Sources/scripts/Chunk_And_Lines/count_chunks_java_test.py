
from count_chunks_java import process_diff

def test_case_1():
    diff_result = process_diff('''nesto1
- azuriranje3
- azuriranje4
+ azuriranje5
+ azuriranje6
- azuriranje7
- azuriranje8
+ azuriranje9
+ azuriranje10	
nesto2''')
    assert diff_result == "0 0 4 0 1 4", f"Should be [0 0 4 0 1 4] not {diff_result}"

def test_case_2():
    diff_result = process_diff('''nesto1
- brisanje1
- brisanje2
- azuriranje3
- azuriranje4
+ azuriranje5
+ azuriranje6	
nesto2''')
    assert diff_result == "0 2 2 0 1 4", f"Should be [0 2 2 0 1 4] not {diff_result}"

def test_case_3():
    diff_result = process_diff('''nesto1
- azuriranje3
- azuriranje4
+ azuriranje5
+ azuriranje6
+ dodavanje1
+ dodavanje2	
nesto2
''')
    assert diff_result == "2 0 2 0 1 4", f"Should be [2 0 2 0 1 4] not {diff_result}"

def test_case_4():
    diff_result = process_diff('''nesto1
- azuriranje1
+ 				
nesto2
- azuriranje3
- azuriranje4
+ 				
+ azuriranje6	
nesto3
''')
    assert diff_result == "0 2 1 0 2 3", f"Should be [0 2 1 0 2 3] not {diff_result}"

def test_case_5():
    diff_result = process_diff('''nesto1
- azuriranje1
- azuriranje2
+ azuriranje3
+ azuriranje1	 
nesto2
''')
    assert diff_result == "0 0 2 1 1 2", f"Should be [0 0 2 1 1 2] not {diff_result}"

def test_case_6():
    diff_result = process_diff('''nesto1
- brisanje1
- brisanje2
- azuriranje3
- azuriranje4
+ azuriranje5
+ brisanje1		
nesto2
''')
    assert diff_result == "0 1 2 1 1 4", f"Should be [0 1 2 1 1 4] not {diff_result}"

def test_case_7():
    diff_result = process_diff('''nesto1
- premestanje1
nesto2
+ premestanje1
nesto3
+ premestanje1	
nesto4
''')
    assert diff_result == "1 0 0 1 3 3", f"Should be [1 0 0 1 3 3] not {diff_result}"

def test_case_8():
    diff_result = process_diff('''nesto1
- azuriranje3
- azuriranje4
+ azuriranje5
+ azuriranje6
+ dodavanje1
+ azuriranje3	
nesto2
''')
    assert diff_result == "1 0 2 1 1 4", f"Should be [1 0 2 1 1 4] not {diff_result}"

def test_case_9():
    diff_result = process_diff('''nesto1
- premestanje1
nesto2
- premestanje1
nesto3
+ premestanje1	
nesto4
''')
    assert diff_result == "0 1 0 1 3 3", f"Should be [0 1 0 1 3 3] not {diff_result}"

def test_case_10():
    diff_result = process_diff('''nesto1
- premestanje1
- premestanje2
nesto2
+ premestanje1
+ premestanje2	
nesto3
''')
    assert diff_result == "0 0 0 2 2 4", f"Should be [0 0 0 2 2 4] not {diff_result}"

def test_case_11():
    diff_result = process_diff('''nesto1
+ premestanje2
- premestanje1
nesto2
+ premestanje1
- premestanje2	
nesto3
''')
    assert diff_result == "0 0 0 2 2 4", f"Should be [0 0 0 2 2 4] not {diff_result}"

def test_case_12():
    diff_result = process_diff('''nesto1
- premestanje1
+ premestanje2
nesto2
- premestanje2
+ premestanje1	
nesto3
''')
    assert diff_result == "0 0 2 2 2 2", f"Should be [0 0 2 2 2 2] not {diff_result}"

def test_case_13():
    diff_result = process_diff('''nesto1
- premestanje1
nesto2
+ dodavanje1
+ premestanje1
+ dodavanje2	
nesto3
''')
    assert diff_result == "2 0 0 1 2 4", f"Should be [2 0 0 1 2 4] not {diff_result}"

def test_case_14():
    diff_result = process_diff('''nesto1
- brisanje1
- premestanje1	
- brisanje2
nesto2
+ premestanje1	
nesto3
''')
    assert diff_result == "0 2 0 1 2 4", f"Should be [0 2 0 1 2 4] not {diff_result}"

def test_case_15():
    diff_result = process_diff('''nesto1
- brisanje1
- premestanje1
- brisanje2
nesto2
+ dodavanje1
+ premestanje1
+ dodavanje2
nesto3
''')
    assert diff_result == "2 2 0 1 2 6", f"Should be [2 2 0 1 2 6] not {diff_result}"

def test_case_16():
    diff_result = process_diff('''nesto1
- premestanje1
nesto2
- azuriranje1
- azuriranje2
+ azurianje3
+ premestanje1
nesto3
''')
    assert diff_result == "0 0 2 1 2 3", f"Should be [0 0 2 1 2 3] not {diff_result}"

def test_case_17():
    diff_result = process_diff('''nesto1
+ premestanje1
nesto2
- premestanje1
- azuriranje2
+ azurianje3
+ azurianje4
nesto3
''')
    assert diff_result == "0 0 2 1 2 3", f"Should be [0 0 2 1 2 3] not {diff_result}"

def test_case_18():
    diff_result = process_diff('''nesto1
+ premestanje1
+ premestanje2
- premestanje3
- premestanje4
nesto3
''')
    assert diff_result == "2 2 0 0 1 4", f"Should be [4 4 0 0 1 4] not {diff_result}"

def test_case_19():
    diff_result = process_diff('''@@ -355,7 +355,8 @@ public class OpenMapRealVector extends AbstractRealVector
     public OpenMapRealVector ebeDivide(double[] v) {
         checkVectorDimensions(v.length);
         OpenMapRealVector res = new OpenMapRealVector(this);
-        Iterator iter = res.entries.iterator();
+        checkVectorDimensions(v.length);
+		Iterator iter = res.entries.iterator();
         while (iter.hasNext()) {
             iter.advance();
             res.setEntry(iter.key(), iter.value() / v[iter.key()]);
@@ -367,7 +368,7 @@ public class OpenMapRealVector extends AbstractRealVector
     public OpenMapRealVector ebeMultiply(RealVector v) {
         checkVectorDimensions(v.getDimension());
         OpenMapRealVector res = new OpenMapRealVector(this);
-        Iterator iter = res.entries.iterator();
+        Iterator iter = entries.iterator();
         while (iter.hasNext()) {
             iter.advance();
             res.setEntry(iter.key(), iter.value() * v.getEntry(iter.key()));
@@ -380,7 +381,7 @@ public class OpenMapRealVector extends AbstractRealVector
     public OpenMapRealVector ebeMultiply(double[] v) {
         checkVectorDimensions(v.length);
         OpenMapRealVector res = new OpenMapRealVector(this);
-        Iterator iter = res.entries.iterator();
+        Iterator iter = entries.iterator();
         while (iter.hasNext()) {
             iter.advance();
             res.setEntry(iter.key(), iter.value() * v[iter.key()]);
''')
    assert diff_result == "0 0 3 1 3 4", f"Should be [0 0 3 1 3 4] not {diff_result}"

def test_case_20():
    diff_result = process_diff('''@@ -86,12 +86,14 @@ class Normalize implements CompilerPass, Callback {
   @Override
   public void process(Node externs, Node root) {
     NodeTraversal.traverse(compiler, root, this);
-    if (MAKE_LOCAL_NAMES_UNIQUE) {
+    
+    removeDuplicateDeclarations(root);
+	if (MAKE_LOCAL_NAMES_UNIQUE) {
       MakeDeclaredNamesUnique renamer = new MakeDeclaredNamesUnique();
       NodeTraversal t = new NodeTraversal(compiler, renamer);
       t.traverseRoots(externs, root);
     }
-    removeDuplicateDeclarations(root);
+
     new PropogateConstantAnnotations(compiler, assertOnChange)
         .process(externs, root);
   }
''')
    assert diff_result == "0 0 0 2 2 4", f"Should be [0 0 0 2 2 4] not {diff_result}"

def test_case_21():
    diff_result = process_diff('''@@ -26,7 +26,10 @@ public class Same extends ArgumentMatcher<Object> implements Serializable {
     public void describeTo(Description description) {
         description.appendText("same(");
         appendQuoting(description);
-        description.appendText(wanted.toString());
+        if (wanted != null) {
+	description.appendText(wanted.toString());
+	}
+
         appendQuoting(description);
         description.appendText(")");
     }
''')
    assert diff_result == "1 0 1 1 1 3", f"Should be [1 0 1 1 1 3] not {diff_result}"

def test_case_22():
    diff_result = process_diff('''@@ -556,17 +556,8 @@ public class XYSeries extends Series implements Cloneable, Serializable {
             existing.setY(y);
         }
         else {
-            // if the series is sorted, the negative index is a result from
-            // Collections.binarySearch() and tells us where to insert the
-            // new item...otherwise it will be just -1 and we should just
-            // append the value to the list...
-            if (this.autoSort) {
-                this.data.add(-index - 1, new XYDataItem(x, y));
-            }
-            else {
-                this.data.add(new XYDataItem(x, y));
-            }
-            // check if this addition will exceed the maximum item count...
+            this.data.add(new XYDataItem(x, y));
+			// check if this addition will exceed the maximum item count...
             if (getItemCount() > this.maximumItemCount) {
                 this.data.remove(0);
             }
''')
    assert diff_result == "0 8 2 2 1 11", f"Should be [0 8 2 2 1 11] not {diff_result}"

def test_case_23():
    diff_result = process_diff('''@@ -1,18 +1,18 @@
 
 linija1
+dodato1
 linija2
+dodato2
+dodato3
 linija3
 linija4
 
 linija5
 linija6
 
-linija7
 
 linija8
 linija9
 
 linija10
-linija11
-linija12
 linija13
\ No newline at end of file
''')
    assert diff_result == "3 3 0 0 4 6", f"Should be [3 3 0 0 4 6] not {diff_result}"

def test_case_24():
    diff_result = process_diff('''@@ -1,13 +1,13 @@
 
 linija1
-linija2
-linija3
+dodato1
+dodato2
 linija4
 
 linija5
-linija6
 
 linija7
+dodato3
 
 linija8
 linija9
''')
    assert diff_result == "1 1 2 0 3 4", f"Should be [1 1 2 0 3 4] not {diff_result}"

def test_case_25():
    diff_result = process_diff('''@@ -1,19 +1,18 @@
 
 linija1
 linija2
-linija3
-linija4
+dodato1
+dodato2
 
-linija5
-linija6
 
 linija7
+dodato3
+
 
 linija8
-linija9
 
 linija10
 linija11
-linija12
 linija13
+linija12
''')
    assert diff_result == "1 3 2 1 6 8", f"Should be [1 3 2 1 6 8] not {diff_result}"

def test_case_26():
    diff_result = process_diff('''@@ -1,19 +1,23 @@
 
 linija1
-linija2
-linija3
+linija5
+linija6
+ linija7
 linija4
 
 linija5
 linija6
 
-linija7
 
 linija8
+dodato1
 linija9
 
 linija10
-linija11
+linija21
+dodato3
+
 linija12
+linija11
 linija13
''')
    assert diff_result == "2 0 3 2 5 8", f"Should be [2 0 3 2 5 8] not {diff_result}"

def test_case_27():
    diff_result = process_diff('''@ @@ -476,7 +476,7 @@ public Vector createVector(String model) ... {
	if (getItemCount() > this.maximumItemCount) {
-        Iterator iter = res.entries.iterator();		
+        Iterator iter = entries.iterator();
	    this.data.remove(0);
-        if (getItemCount() > this.maximumItemCount) {	
-		checkVectorDimensions(v.length);	
+        if (this.isCountable && getItemCount() > this.maxItemCount) {	
+		checkVectorDirection(v.direction);
+		updateVectorDirection(direction);
  }

@@ -486,6 +486,9 @@ public List<XYDataItem> listItems()  ... {     
	if (this.autoSort) {
+ 	     this.data.remove(lastIndex);
	     this.data.remove(0);
+ 	     label = vector.text;
+          this.data.add(-index - 1, new XYDataItem(x, y));
+	     existing.setY(y);
      }
-     else {            
-          this.data.add(new XYDataItem(x, y));            
-     }            
	...
+	     checkVectorDimensions(v.length);	     
      ...
  }

@@ -486,6 +486,9 @@ public String getDescription()  ... {     
	    ...
-            label = vector.text;
	    ...
  }
''')
    assert diff_result == "4 3 3 2 7 13", f"Should be [4 3 3 2 7 13] not {diff_result}"    


if __name__ == "__main__":
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()
    test_case_7()
    test_case_8()
    test_case_9()
    test_case_10()
    test_case_11()
    test_case_12()
    test_case_13()
    test_case_14()
    test_case_15()
    test_case_16()
    test_case_17()
    test_case_18()
    test_case_19()
    test_case_20()
    test_case_21()
    test_case_22()
    test_case_23()
    test_case_24()
    test_case_25()
    test_case_26()
    test_case_27()
    print("Everything passed")
