// Stanford TMT Example 2 - Learning an LDA model
// http://nlp.stanford.edu/software/tmt/0.3/

// tells Scala where to find the TMT classes
import scalanlp.io._;
import scalanlp.stage._;
import scalanlp.stage.text._;
import scalanlp.text.tokenize._;
import scalanlp.pipes.Pipes.global._;

import edu.stanford.nlp.tmt.stage._;
import edu.stanford.nlp.tmt.model.SymmetricDirichletParams;
import edu.stanford.nlp.tmt.model.lda._;
import edu.stanford.nlp.tmt.model.llda._;

import java.io.File;
import edu.stanford.nlp.tmt.learn._;
import edu.stanford.nlp.tmt.model._;



val source = CSVFile("lemmatized.csv") ~> IDColumn(1);

val tokenizer = {
  SimpleEnglishTokenizer()             // tokenize on space and punctuation
//  SimpleEnglishTokenizer() ~>            // tokenize on space and punctuation
//  CaseFolder() ~>                        // lowercase everything
//  WordsAndNumbersOnlyFilter() ~>         // ignore non-words and non-numbers
//  MinimumLengthFilter(3)                 // take terms with >=3 characters
}

val text = {
  source ~>                              // read from the source file
  Column(2) ~>                           // select column containing text
  TokenizeWith(tokenizer) ~>             // tokenize with tokenizer above
  TermCounter() ~>                       // collect counts (needed below)
  TermMinimumDocumentCountFilter(5) ~>   // filter terms in <4 docs
  TermDynamicStopListFilter(100) ~>       // filter out 30 most common terms
  DocumentMinimumLengthFilter(5)         // take only docs with >=5 terms
}

for (i <- text) {
    print(i.id.toString + ",")
    for (w <- i.value) {
        print(" " + w)
    }
    println()
}
