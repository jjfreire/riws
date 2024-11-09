import React from "react";

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import {
  buildAutocompleteQueryConfig,
  buildFacetConfigFromConfig,
  buildSearchOptionsFromConfig,
  buildSortOptionsFromConfig,
  getConfig,
  getFacetFields
} from "./config/config-helper";

const { hostIdentifier, searchKey, endpointBase, engineName } = getConfig();
const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "jobs"
});
const config = {
    searchQuery: {

      //Campos por los que se puede hacer la búsqueda
      search_fields: {
        title: {
          weight: 3
        },
        description: {
          weight: 2
        },
        salary: {
          weight: 2
        },
        location: {
          weight: 1
        },
        company: {
          weight: 1
        },
        workday: {
          weight: 1
        },
        modality: {
          weight: 2
        },
        duration: {
          weight: 1
        }
      },

      //Campos que se muestran de los resultados de la búsqueda
      result_fields: {
        title: {
          snippet: {}
        },
        description: {
          snippet: {}
        },
        salary: {
          raw: {}
        },
        location: {
          raw: {}
        },
        company: {
          raw: {}
        },
        workday: {
          raw: {}
        },
        modality: {
          raw: {}
        },
        duration: {
          raw: {}
        },
        link: {
          raw: {}
        },

      },

      //Filtros que quieres que actuen con un OR
      disjunctiveFacets: ["modality.keyword", "workday.keyword", "location.keyword", "company.keyword", "duration.keyword"],

      //Configuración de los filtros
      facets: {
        "modality.keyword": { type: "value" },
        "workday.keyword": { type: "value" },
        "location.keyword": { type: "value" },
        "company.keyword": { type: "value" },
        "duration.keyword": { type: "value" },
      }
    },
    
    autocompleteQuery: {
      results: {
        resultsPerPage: 5,
        search_fields: {
          "title": {
            weight: 3
          }
        },
        result_fields: {
          title: {
            snippet: {
              size: 100,
              fallback: true
            }
          },
          link: {
            raw: {}
          }
        }
      },

      //Para usar suggestions tendríamos que tener un campo de tipo completion en el índice
    
    },
    apiConnector: connector,
    alwaysSearchOnInitialLoad: true
  
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={
                    <SearchBox
                      autocompleteMinimumCharacters={3}
                      autocompleteResults={{
                        linkTarget: "_blank",
                        sectionTitle: "Results",
                        titleField: "title",
                        urlField: "url",
                        shouldTrackClickThrough: true
                      }}
                      autocompleteSuggestions={true}
                      debounceLength={0}
                    />
                  }
                  sideContent={
                    <div>
                      <Facet key={"1"} field={"modality.keyword"} label={"Modality"} />
                      <Facet key={"2"} field={"workday.keyword"} label={"Workday"} />
                      <Facet key={"3"} field={"location.keyword"} label={"Location"} />
                      <Facet key={"4"} field={"company.keyword"} label={"Company"} />
                      <Facet key={"5"} field={"duration.keyword"} label={"Duration"} />
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField={getConfig().titleField}
                      urlField={getConfig().urlField}
                      thumbnailField={getConfig().thumbnailField}
                      shouldTrackClickThrough={true}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
