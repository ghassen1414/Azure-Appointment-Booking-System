import React, { useState, ChangeEvent, FormEvent } from "react";

interface FormField {
  name: string;
  label: string;
  type: string;
  required?: boolean;
}

interface GenericFormProps {
  fields: FormField[];
  onSubmit: (formData: Record<string, string>) => void;
  submitButtonText?: string;
}

const GenericForm: React.FC<GenericFormProps> = ({
  fields,
  onSubmit,
  submitButtonText = "Submit",
}) => {
  const initialFormState = fields.reduce((acc, field) => {
    acc[field.name] = "";
    return acc;
  }, {} as Record<string, string>);

  const [formData, setFormData] =
    useState<Record<string, string>>(initialFormState);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(formData);
    // Optionally reset form: setFormData(initialFormState);
  };

  return (
    <form onSubmit={handleSubmit}>
      {fields.map((field) => (
        <div key={field.name} style={{ marginBottom: "10px" }}>
          <label htmlFor={field.name}>{field.label}:</label>
          <br />
          <input
            type={field.type}
            id={field.name}
            name={field.name}
            value={formData[field.name]}
            onChange={handleChange}
            required={field.required}
            style={{ padding: "5px", width: "200px" }}
          />
        </div>
      ))}
      <button type="submit">{submitButtonText}</button>
    </form>
  );
};

export default GenericForm;
