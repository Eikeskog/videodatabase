import React from 'react';
import Checkbox from '../../../../common/components/Checkbox';
import CheckboxList from '../../../../common/components/CheckboxList';

export const renderCheckboxList = ({
  filterType,
  initialValues,
  activeSearchfilters,
  toggleActiveSearchfilter,
}) => (
  <CheckboxList>

    { activeSearchfilters?.[filterType]
      && Object.keys(activeSearchfilters[filterType])
        .filter((id) => !Object.keys(initialValues).includes(id))
        .map((id) => {
          const label = activeSearchfilters[filterType][id];
          return (
            <Checkbox
              key={id}
              id={id}
              label={label}
              checked
              onClick={() => toggleActiveSearchfilter(
                filterType,
                id,
                label,
              )}
            />
          );
        })}

    { initialValues
      && Object.keys(initialValues)
        .map((id) => {
          const label = initialValues[id];
          return (
            <Checkbox
              key={id}
              id={id}
              label={label}
              checked={!!activeSearchfilters?.[filterType]?.[id]}
              onClick={() => toggleActiveSearchfilter(
                filterType,
                id,
                label,
              )}
            />
          );
        })}

  </CheckboxList>
);

export const renderTypingHints = ({
  typingHints,
  filterType,
  activeSearchfilters,
  toggleActiveSearchfilter,
}) => {
  if (typingHints.isLoading) return <span>Laster data ...</span>;

  if (!typingHints.results.length) return <span>Ingen treff</span>;

  return (
    <CheckboxList>

      {typingHints.results.map((hint) => (
        <Checkbox
          key={hint.id}
          id={hint.id}
          label={hint.label}
          checked={!!activeSearchfilters?.[filterType]?.[hint.id]}
          onClick={() => toggleActiveSearchfilter(
            filterType,
            hint.id,
            hint.label,
          )}
        />
      ))}

    </CheckboxList>
  );
};
