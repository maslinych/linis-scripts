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

// turn the text into a dataset ready to be used with LDA
val dataset = LDADataset(text);

// define the model parameters
val params = LDAModelParams(numTopics = 100, dataset = dataset,
  topicSmoothing = SymmetricDirichletParams(0.01),
  termSmoothing = SymmetricDirichletParams(0.01)
);

// Name of the output model folder to generate
val modelPath = file("lda100");

// Trains the model: the model (and intermediate models) are written to the
// output folder.  If a partially trained model with the same dataset and
// parameters exists in that folder, training will be resumed.
//TrainCVB0LDA(params, dataset, output=modelPath, maxIterations=1000);

// To use the Gibbs sampler for inference, instead use
//TrainGibbsLDA(params, dataset, output=modelPath, maxIterations=1500);

  def ResumableTrainGibbsLDA(modelParams : LDAModelParams, dataset : Iterable[LDADocumentParams], output : File, maxIterations : Int = 1500) : GibbsLDA = {
    val modeler = SerialModeler(GibbsLDA);
    modeler.train(modelParams, dataset, output, saveDataState = true, maxIterations = maxIterations);
    if (output != null) {
      val table : Iterable[(String,Array[Double])] =
        modeler.data.view.map(doc => (doc.id,doc.signature));
      CSVFile(output, "document-topic-distributions.csv").write(table);
    }   
    modeler.model.get;
  }

ResumableTrainGibbsLDA(params, dataset, output=modelPath, maxIterations=1500);

